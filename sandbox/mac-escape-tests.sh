#!/usr/bin/env bash
# ============================================================================================
# mac-escape-tests.sh - macOS (Seatbelt/sandbox-exec) acceptance gates for the augmented launcher.
#
# Mirrors serve/deploy/layerc-escape-tests.sh, but invokes the macOS confinement WRAPPER
# (confine-run.sh, its darwin branch) DIRECTLY - the wrapper IS the boundary; there is nothing to run it
# "through". Each gate must fail closed before the macOS tier is trusted to confine.
#
# POSITIVE CONTROLS (adversarial H1): a deny gate on an offline / feature-less box would score a
# spurious PASS (the escape "failed" only because the resource was never reachable). So EACH deny
# gate is paired with a BASELINE that must SUCCEED in the same run (egress reachable under
# --egress host; a write succeeding inside $SCR; a cred read succeeding with NO --exclude). A gate
# scores PASS only when baseline=reachable AND confined=denied; otherwise INDETERMINATE, never PASS.
#
# TRUST MODEL: sandbox-exec's kernel step is `sandbox_apply`. If an OUTER sandbox is active (e.g.
# Claude Code's own Bash-tool sandbox), a NESTED sandbox_apply is refused and the guest never starts.
# A nesting probe sets NESTED=1 and then EVERY profile-dependent gate is forced UNTRUSTED
# unconditionally (M3 - we do NOT depend on matching Apple's exact error string). Kernel-enforced
# checks that do NOT need sandbox_apply (RLIMIT_CPU via ulimit) stay trustworthy. A false PASS is
# worse than an N/A or UNTRUSTED.
# ============================================================================================
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
WRAP="$HERE/confine-run.sh"   # the emitted launcher (was the never-emitted confine-run.macos-ref.sh)
pass=0; fail=0; na=0; untrusted=0; indet=0
ok(){   echo "  PASS          $1"; pass=$((pass+1)); }
no(){   echo "  FAIL          $1"; fail=$((fail+1)); }
skip(){ echo "  N/A           $1  ($2)"; na=$((na+1)); }
unt(){  echo "  UNTRUSTED     $1  ($2)"; untrusted=$((untrusted+1)); }
ind(){  echo "  INDETERMINATE $1  ($2)"; indet=$((indet+1)); }

[ -x "$WRAP" ] || { echo "wrapper not found/executable: $WRAP"; exit 2; }
echo "== macOS escape tests =="
echo "host: $(uname -sr) $(uname -m)   wrapper: $WRAP"

# -- nesting probe: is an OUTER sandbox blocking sandbox_apply right now? -----------------------
NESTED=0
TRIV="$HERE/.nesting-probe.sb"
printf '(version 1)\n(allow default)\n' > "$TRIV"
nprobe="$(sandbox-exec -f "$TRIV" /bin/echo NESTOK 2>&1)"
rm -f "$TRIV"
if ! printf '%s' "$nprobe" | grep -q NESTOK; then
  NESTED=1
  echo "NESTING: DETECTED - sandbox_apply blocked by an outer sandbox ($nprobe)."
  echo "         ALL profile-dependent gates are forced UNTRUSTED; re-run in an unconfined operator terminal."
else
  echo "NESTING: none detected - sandbox_apply works; profile-dependent gates are trustworthy here."
fi

SCR="$HERE/.mac-test-scratch"; SIB="$HERE/.mac-test-sibling"
rm -rf "$SCR" "$SIB"; mkdir -p "$SCR" "$SIB"; echo SECRET > "$SIB/creds.txt"
OUT_OF_SCRATCH="$HERE/.mac-test-should-not-write"; rm -f "$OUT_OF_SCRATCH"

# run a probe through the wrapper; echo its LAST line, or "OUTERWALL" if the outer sandbox blocked it.
runwrap(){ # args: -- passed verbatim to the wrapper
  local out; out="$(bash "$WRAP" "$@" 2>&1)"
  if printf '%s' "$out" | grep -qi 'sandbox_apply: Operation not permitted'; then echo OUTERWALL
  else printf '%s' "$out" | tail -1; fi
}

# ---- Gate 1: write confinement (baseline: write inside $SCR succeeds; confined: outside denied) ---
echo "[1] filesystem write confinement (H1 positive control)"
if [ "$NESTED" = 1 ]; then
  unt "fs write confinement" "outer sandbox forces UNTRUSTED; guest cannot start"
else
  base="$(runwrap --scratch "$SCR" --egress deny -- /bin/bash -c 'echo x > "'"$SCR"'/inbounds" 2>/dev/null && echo WROTE || echo failed')"
  conf="$(runwrap --scratch "$SCR" --egress deny -- /bin/bash -c '(echo x > "'"$OUT_OF_SCRATCH"'") 2>/dev/null && echo WROTE || echo denied')"
  if [ "$base" = OUTERWALL ] || [ "$conf" = OUTERWALL ]; then unt "fs write confinement" "outer sandbox_apply wall"
  elif [ "$base" != WROTE ]; then ind "fs write confinement" "baseline write inside scratch did NOT succeed (base=$base); cannot trust the deny"
  elif [ "$conf" = denied ] && [ ! -f "$OUT_OF_SCRATCH" ]; then ok "write inside scratch OK (baseline), write outside scratch DENIED (confined)"
  else no "write escaped scratch (baseline=$base confined=$conf, file-exists=$([ -f "$OUT_OF_SCRATCH" ] && echo yes || echo no))"; fi
fi
rm -f "$OUT_OF_SCRATCH"

# ---- Gate 2: credential read confinement (baseline: read w/o --exclude; confined: with --exclude) -
echo "[2] credential/sibling read confinement (H1 positive control)"
if [ "$NESTED" = 1 ]; then
  unt "cred read confinement" "outer sandbox forces UNTRUSTED; guest cannot start"
else
  base="$(runwrap --scratch "$SCR" --egress deny -- /bin/bash -c 'cat "'"$SIB"'/creds.txt" >/dev/null 2>&1 && echo READ || echo failed')"
  conf="$(runwrap --scratch "$SCR" --egress deny --exclude "$SIB" -- /bin/bash -c 'cat "'"$SIB"'/creds.txt" >/dev/null 2>&1 && echo READ || echo denied')"
  if [ "$base" = OUTERWALL ] || [ "$conf" = OUTERWALL ]; then unt "cred read confinement" "outer sandbox_apply wall"
  elif [ "$base" != READ ]; then ind "cred read confinement" "baseline read (no --exclude) did NOT succeed (base=$base); cannot trust the deny"
  elif [ "$conf" = denied ]; then ok "read succeeds without --exclude (baseline), DENIED with --exclude (confined)"
  else no "sibling read was NOT denied under --exclude (baseline=$base confined=$conf)"; fi
fi

# ---- Gate 3: raw egress confinement (baseline: reachable under host; confined: denied under deny) --
echo "[3] raw egress confinement (H1 positive control)"
EPROBE_HOST='e=unreachable; (exec 3<>/dev/tcp/1.1.1.1/443) 2>/dev/null && e=REACHED; echo $e'
EPROBE_DENY='e=denied; (exec 3<>/dev/tcp/1.1.1.1/443) 2>/dev/null && e=REACHED; echo $e'
if [ "$NESTED" = 1 ]; then
  unt "raw egress confinement" "outer sandbox forces UNTRUSTED; guest cannot start"
else
  base="$(runwrap --scratch "$SCR" --egress host -- /bin/bash -c "$EPROBE_HOST")"
  conf="$(runwrap --scratch "$SCR" --egress deny -- /bin/bash -c "$EPROBE_DENY")"
  if [ "$base" = OUTERWALL ] || [ "$conf" = OUTERWALL ]; then unt "raw egress confinement" "outer sandbox_apply wall"
  elif [ "$base" != REACHED ]; then ind "raw egress confinement" "baseline egress under --egress host was NOT reachable (base=$base); box may be offline - cannot trust the deny"
  elif [ "$conf" = denied ]; then ok "egress reachable under --egress host (baseline), DENIED under --egress deny (confined)"
  else no "egress was NOT denied under --egress deny (baseline=$base confined=$conf)"; fi
fi

# ---- Gate 4: setuid-exec denied (baseline: /bin/echo runs; confined: /usr/bin/sudo denied) --------
# sudo -V prints "Sudo version ..." WITHOUT privilege, so seeing it => exec ALLOWED (FAIL). Baseline
# execs a NON-denylisted binary to prove exec works at all under the profile.
echo "[4] setuid-exec denied - direct literal (H1 positive control)"
DOWNGRADE=0
if [ "$NESTED" = 1 ]; then
  unt "setuid-exec (direct)" "outer sandbox forces UNTRUSTED; guest cannot start"
elif [ ! -x /usr/bin/sudo ]; then
  skip "setuid-exec (direct)" "/usr/bin/sudo absent"
else
  base="$(runwrap --scratch "$SCR" --egress deny -- /bin/echo EXEC_BASELINE_OK)"
  conf="$(runwrap --scratch "$SCR" --egress deny -- /usr/bin/sudo -V)"
  if [ "$base" = OUTERWALL ] || [ "$conf" = OUTERWALL ]; then unt "setuid-exec (direct)" "outer sandbox_apply wall"
  elif [ "$base" != EXEC_BASELINE_OK ]; then ind "setuid-exec (direct)" "baseline exec of /bin/echo did NOT run (base=$base); cannot trust the deny"
  elif printf '%s' "$conf" | grep -qi 'Sudo version'; then no "setuid /usr/bin/sudo EXECUTED under confinement (denylist not enforced)"
  else ok "non-denylisted exec runs (baseline), /usr/bin/sudo DENIED by process-exec* denylist (confined)"; fi
fi

# ---- Gate 4b: H2 setuid bypass via SYMLINK-in-scratch to /usr/bin/sudo ----------------------------
echo "[4b] setuid-exec denied - symlink alias (H2)"
if [ "$NESTED" = 1 ]; then
  unt "setuid-exec (symlink)" "outer sandbox forces UNTRUSTED; guest cannot start"
elif [ ! -x /usr/bin/sudo ]; then
  skip "setuid-exec (symlink)" "/usr/bin/sudo absent"
else
  ln -sf /usr/bin/sudo "$SCR/sudo_symlink"
  conf="$(runwrap --scratch "$SCR" --egress deny -- "$SCR/sudo_symlink" -V)"
  if [ "$conf" = OUTERWALL ]; then unt "setuid-exec (symlink)" "outer sandbox_apply wall"
  elif printf '%s' "$conf" | grep -qi 'Sudo version'; then no "BYPASS: symlink-in-scratch to /usr/bin/sudo EXECUTED (literal-path denylist evaded)"; DOWNGRADE=1
  else ok "symlink-in-scratch to /usr/bin/sudo DENIED (vnode resolves to the denied literal)"; fi
  rm -f "$SCR/sudo_symlink"
fi

# ---- Gate 4c: H2 setuid bypass via HARDLINK-in-scratch to /usr/bin/sudo ---------------------------
echo "[4c] setuid-exec denied - hardlink alias (H2)"
if [ "$NESTED" = 1 ]; then
  unt "setuid-exec (hardlink)" "outer sandbox forces UNTRUSTED; guest cannot start"
elif [ ! -x /usr/bin/sudo ]; then
  skip "setuid-exec (hardlink)" "/usr/bin/sudo absent"
elif ! ln /usr/bin/sudo "$SCR/sudo_hardlink" 2>/dev/null; then
  skip "setuid-exec (hardlink)" "volume does not permit a hardlink from scratch to /usr/bin (SSV/cross-volume) - bypass vector not constructible here"
else
  conf="$(runwrap --scratch "$SCR" --egress deny -- "$SCR/sudo_hardlink" -V)"
  if [ "$conf" = OUTERWALL ]; then unt "setuid-exec (hardlink)" "outer sandbox_apply wall"
  elif printf '%s' "$conf" | grep -qi 'Sudo version'; then no "BYPASS: hardlink-in-scratch to /usr/bin/sudo EXECUTED (new path evades the literal denylist)"; DOWNGRADE=1
  else ok "hardlink-in-scratch to /usr/bin/sudo DENIED"; fi
  rm -f "$SCR/sudo_hardlink"
fi
[ "$DOWNGRADE" = 1 ] && echo "  >> H2 DOWNGRADE: an alias BYPASSED the denylist. Relabel setuid protection to 'blocks only direct literal-path invocation' in the launcher comment AND the runbook."

# ---- Gate 5: CPU cap fires (--cpu-max 2 on a busy loop). -----------------------------------------
echo "[5] CPU cap fires (--cpu-max 2, busy loop)"
busy='python3 -c "x=0
while True: x+=1"'
if [ "$NESTED" = 1 ]; then
  unt "CPU cap via wrapper" "outer sandbox forces UNTRUSTED (M3); mechanism verified independently below"
else
  cres="$(bash "$WRAP" --scratch "$SCR" --egress deny --cpu-max 2 -- /bin/bash -c "$busy" 2>&1; echo "rc=$?")"
  crc="$(printf '%s' "$cres" | sed -n 's/.*rc=\([0-9]*\)$/\1/p' | tail -1)"
  if printf '%s' "$cres" | grep -qi 'sandbox_apply: Operation not permitted'; then unt "CPU cap via wrapper" "outer sandbox_apply wall"
  elif [ "${crc:-0}" = "152" ] || [ "${crc:-0}" = "137" ]; then ok "busy loop terminated by RLIMIT_CPU through the wrapper (rc=$crc; 152=SIGXCPU,137=SIGKILL)"
  else no "busy loop NOT CPU-capped through the wrapper (rc=${crc:-?})"; fi
fi
# Mechanism check - RLIMIT_CPU is kernel-enforced and does NOT need sandbox_apply, so it is
# TRUSTWORTHY even while nested. Proves the primitive the wrapper's --cpu-max relies on.
mrc="$( ( ulimit -t 2; python3 -c "x=0
while True: x+=1" ) >/dev/null 2>&1; echo $? )"
if [ "$mrc" = "152" ] || [ "$mrc" = "137" ]; then ok "RLIMIT_CPU mechanism (ulimit -t 2) terminates a busy loop (rc=$mrc) - TRUSTWORTHY, sandbox_apply-independent"
else no "RLIMIT_CPU mechanism did NOT terminate the busy loop (rc=$mrc)"; fi

# ---- Gate 6: NPROC cap - meaningful ONLY under a dedicated uid. -----------------------------------
echo "[6] NPROC cap (RLIMIT_NPROC)"
nwarn="$(bash "$WRAP" --scratch "$SCR" --egress deny --nproc-max 64 --check -- /bin/echo hi 2>&1)"
if printf '%s' "$nwarn" | grep -qi 'self-DoS knob'; then
  skip "NPROC cap" "wrapper honestly flags it: isolates a tenant ONLY under a dedicated uid; on this shared uid it is a self-DoS knob, not isolation - see dedicated-uid-provisioning.example.sh"
else no "wrapper did NOT emit the required NPROC dedicated-uid caveat"; fi

# ---- Gate 7: memory cap - EXPECTED-UNCAPPED on macOS (fail-honest, N/A not FAIL). -----------------
echo "[7] memory cap (--mem-max) - expected UNCAPPED on macOS"
memwarn="$(bash "$WRAP" --scratch "$SCR" --egress deny --mem-max 128 --check -- /bin/echo hi 2>&1)"
if printf '%s' "$memwarn" | grep -qi 'MEMORY UNCAPPED'; then
  skip "memory cap" "EXPECTED-UNCAPPED - wrapper loudly declares memory is NOT enforced on macOS (interface-only, fail-honest); hard cap needs VM/container/Linux. HONEST N/A, not a FAIL"
else no "wrapper did NOT loudly declare memory UNCAPPED (fail-honest contract broken)"; fi

# ---- Gate 8: control plane (F-4 parity with Linux, 2026-10-07) ---------------------------------
# Baseline: a plain write inside the writable root succeeds. Confined: the decision-signing switch, the
# verify-key store and the team marker can't be written, and the ancestor holding them can't be renamed.
echo "[8] control-plane write protection (switch, verify keys, marker, ancestor rename)"
if [ "$NESTED" = 1 ]; then
  unt "control plane" "outer sandbox forces UNTRUSTED; guest cannot start"
else
  CPR="$SCR/.claude/agents/references"; mkdir -p "$CPR/authorized-verify-keys" "$SCR/.claude/hooks"
  echo '{"enforce_decision_signing": true}' > "$CPR/agent-privilege.json"; echo '{}' > "$CPR/build-log.json"
  for f in security-approvers.txt authorized-managers.txt management-authority.json; do echo x > "$CPR/$f"; done
  printf -- '---\nname: o\n---\n' > "$SCR/.claude/agents/orchestrator.md"; echo '#' > "$SCR/.claude/hooks/constitutional-gate.py"
  base="$(runwrap --scratch "$SCR" --egress deny -- /bin/bash -c 'echo x > "'"$SCR"'/cp-baseline" 2>/dev/null && echo WROTE || echo failed')"
  conf="$(runwrap --scratch "$SCR" --egress deny -- /bin/bash -c '
    r=""
    (echo pwn > "'"$CPR"'/agent-privilege.json") 2>/dev/null && r="$r switch"
    (touch "'"$CPR"'/authorized-verify-keys/planted.pub.pem") 2>/dev/null && r="$r verify-key"
    (rm "'"$CPR"'/build-log.json") 2>/dev/null && r="$r marker"
    (mv "'"$CPR"'" "'"$SCR"'/.claude/agents/moved") 2>/dev/null && r="$r rename"
    [ -z "$r" ] && echo denied || echo "ESCAPED:$r"')"
  if [ "$base" = OUTERWALL ] || [ "$conf" = OUTERWALL ]; then unt "control plane" "outer sandbox_apply wall"
  elif [ "$base" != WROTE ]; then ind "control plane" "baseline write inside the root did NOT succeed (base=$base)"
  elif [ "$conf" = denied ] && grep -q true "$CPR/agent-privilege.json"; then ok "baseline write OK; switch, verify-key plant, marker delete and ancestor rename all DENIED"
  else no "control plane writable (confined=$conf)"; fi
fi

# ---- Gate 8b: a root under /private/tmp can't be renamed away to reach its control plane ---------
echo "[8b] root rename-away under /private/tmp (writable subpath) is denied"
if [ "$NESTED" = 1 ]; then
  unt "root rename-away" "outer sandbox forces UNTRUSTED"
else
  TB="$(mktemp -d /private/tmp/agentteams-gate8b.XXXXXX)"; TP="$TB/proj"; TR="$TP/.claude/agents/references"
  mkdir -p "$TR/authorized-verify-keys" "$TP/.claude/hooks" "$TB/scr"
  echo '{"enforce_decision_signing": true}' > "$TR/agent-privilege.json"; echo '{}' > "$TR/build-log.json"
  for f in security-approvers.txt authorized-managers.txt management-authority.json; do echo x > "$TR/$f"; done
  printf -- '---\nname: o\n---\n' > "$TP/.claude/agents/orchestrator.md"; echo '#' > "$TP/.claude/hooks/constitutional-gate.py"
  conf="$(runwrap --scratch "$TB/scr" --writable "$TP" --egress deny -- /bin/bash -c '
    echo x > "'"$TP"'/cp-baseline" 2>/dev/null || { echo NOBASE; exit 0; }
    (mv "'"$TP"'" "'"$TB"'/moved") 2>/dev/null && { echo pwn > "'"$TB"'/moved/.claude/agents/references/agent-privilege.json"; mv "'"$TB"'/moved" "'"$TP"'"; echo RENAMED; exit 0; }
    echo denied')"
  if [ "$conf" = OUTERWALL ]; then unt "root rename-away" "outer sandbox_apply wall"
  elif [ "$conf" = NOBASE ]; then ind "root rename-away" "baseline write inside the root did NOT succeed"
  elif [ "$conf" = denied ] && grep -q true "$TR/agent-privilege.json"; then ok "root under /private/tmp can't be renamed away; switch intact"
  else no "root renamed away and control plane written (confined=$conf)"; fi
  rm -rf "$TB"
fi

rm -rf "$SCR" "$SIB" "$OUT_OF_SCRATCH"
echo
echo "SUMMARY: $pass pass, $fail fail, $na n/a, $untrusted untrusted, $indet indeterminate"
if [ "$NESTED" = 1 ]; then
  echo "NOTE: profile-dependent gates are UNTRUSTED here (outer sandbox). Authoritative run REQUIRES an"
  echo "      unconfined operator terminal WITH internet reachability (for the egress positive control)."
fi
echo "Only FAIL blocks trust. UNTRUSTED = not proven here (nesting). INDETERMINATE = positive control"
echo "did not hold (offline/feature-less box), so the paired deny cannot be trusted - re-run properly."
[ "$fail" -eq 0 ] && exit 0 || exit 1
