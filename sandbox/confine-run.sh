#!/usr/bin/env bash
# ============================================================================================
# sandbox/confine-run.sh - provider-agnostic outside-in confinement launcher (Layer C/D).
#
# Wraps ANY agentic provider/interface command - `goose run ...`, a `claude`/`codex`/`copilot` CLI, a
# python agent, an MCP server - in an OS-enforced boundary. It confines a *process*, not a specific
# harness, and OS-dispatches:
#
#   * Linux  -> bwrap read-only-root + (netns) + NoNewPrivs   (ENFORCEMENT-VERIFIED by a live-kernel bwrap escape/deny test)
#   * macOS  -> sandbox-exec with a path-agnostic Seatbelt profile  (INERT/`--check` here;
#              ENFORCEMENT-UNVERIFIED off a macOS host - no green claim without an on-mac deny test)
#   * other  -> FAIL CLOSED (never runs a command while labeled "confined")
#
# PROVENANCE / SOURCE OF TRUTH (operator directive 2026-08-31): this launcher is the FRAMEWORK-NEUTRAL
# reference implementation that agentteams is to EMIT (Linux "works like Seatbelt": an emitted OS-
# confinement boundary, analogous to the macOS `sandbox-exec -f profile <argv>` path). The emitter lives
# in agentteams (`agentteams/frameworks/_linux_sandbox_emit.py`), which emits it verbatim to a
# consuming project's repo-root `sandbox/confine-run.sh`. agentteams is the single source of truth:
# a consuming project keeps its copy BYTE-IDENTICAL to the emitted artifact (guard drift with a
# sha256 pin), and never forks it. It confines ANY provider (goose/claude/codex/copilot) equally -
# NO harness is preferred here; any harness preference belongs in the consuming project, never in
# this launcher.  NOTE: this file is intentionally ASCII-only so the sha256 parity pin cannot drift
# through a UTF-8 re-encode.
#
# Policy (POLA / fail-closed): read-only root; ONLY --scratch writable; /tmp scratch; credential dirs
# (~/.ssh ~/.aws ~/.gnupg ~/.kube ~/.config/gcloud ~/.azure), the operator decision-signing private-key
# dir ~/.config/agentteams/keys, any legacy ~/.config/agentteams/*.pem key file, and --exclude paths
# (directories or files) read-excluded; egress
# deny(default)/proxy(root+netns, OOB)/host(fs-confined only). --writable adds a rw path; --setenv
# passes VAR=VAL into the guest. The guest environment is DEFAULT-DENY: it inherits none of the
# launcher's env; only a benign built-in allowlist (plus --env-allow NAMEs and explicit --setenv
# values) is passed, so an operator signing-key path / *_SIGNING_KEY secret never leaks in. This
# closes NOTHING re T6 + host-as-TCB (bounded, never closed); seccomp/Landlock is a further layer.
#
# Usage:
#   sandbox/confine-run.sh --scratch DIR [--egress deny|proxy|host] [--proxy ADDR:PORT]
#          [--netns NAME] [--exclude PATH]... [--writable PATH]... [--coord-root PATH]... [--protect PATH]...
#          [--setenv VAR=VAL]... [--env-allow VAR]... [--cpu-max SEC] [--nproc-max N] [--mem-max MiB]
#          [--protect-prompt-roots] [--check] -- CMD [ARGS...]
#
# --coord-root PATH (repeatable): bind a sibling/adjacent-repo write root for cross-repo
#   coordination. UNLIKE --writable (which mkdir -p's a missing path), a coordination target
#   that does not exist is a FAIL-CLOSED error (a missing sibling repo is a misconfiguration,
#   not something to auto-create). Existence is verified in the OS-independent block BEFORE OS
#   dispatch, so a missing target is a clean exit-2, never a bwrap sandbox-init crash (D-3).
#
# CONTROL PLANE (F-4, 2026-09-30 Linux/bwrap; macOS Seatbelt 2026-10-07): inside every writable root (--scratch,
#   --writable, --coord-root) each EXISTING agentteams control-plane path (CONTROL_PLANE_REL below:
#   the enforce_decision_signing switch, the gate hook, the verify-key store, the approver/manager
#   rosters and management config (PR-D), the goose profile, and each team's build-log marker) is
#   --ro-bind'ed, and each of its ancestor dirs below the root gets a read-write SELF-bind so it
#   becomes a mount point: renaming it away (`mv .claude .claude.old`, then plant a tree) fails
#   EBUSY, while writes inside it still work. Order: rw roots, ancestor self-binds, ro-binds, masks.
#   Every protected path is realpath'd and a SYMLINK anywhere on it is refused (die). A framework's
#   entries are REQUIRED only when that framework holds an agentteams team, marked by
#   <agents dir>/references/build-log.json (TEAM_MARKER_REL); a hand-written .claude/agents without
#   it is skipped. Each present marker is itself ro-bound, so it cannot be deleted from inside to
#   disable the check. The approver/manager rosters are required only when that team's switch is
#   present. A required entry that is absent is a DIE (a writable parent would let the process create
#   it); anything else absent is skipped. The project-root references/security-approvers.txt (the
#   grant roster) is protect-if-present only. Four team dirs are covered (TEAM_DIRS_REL): .claude/agents,
#   .goose/recipes, .github/agents (copilot) and .codex/agents (codex); .codex/config.toml is
#   protect-if-present. Only .github/agents/* maps to a team: .github/workflows is never protected,
#   and its self-bound ancestor .github stays writable. --protect PATH (repeatable) ro-binds an extra path,
#   e.g. a whole `.claude`; a missing --protect path is a die, never mkdir.
#   Status: mechanism-verified (raw bwrap probes), product-unverified. macOS (2026-10-07): the same set is
#   collected and written into the Seatbelt profile AFTER the allows: (deny file-write* (subpath P)) for each
#   protected path and (deny file-write* (literal A)) for each ancestor below a writable root (rename lock).
#
# --protect-prompt-roots (OPT-IN, follow-up #8 phase 2, 2026-10-01; Linux/bwrap, and macOS since 2026-10-07): also
#   ro-bind each EXISTING prompt root (PROMPT_ROOTS_REL below: the files other harnesses read as
#   instructions) under every writable root, with the same ancestor self-binds and symlink refusal
#   (cp_real). Protect-if-present: an absent root is skipped, never required, never a die. A
#   symlinked root (e.g. CLAUDE.md -> AGENTS.md) is a die: move it or drop the flag. Off by default
#   because it blocks confined agents from authoring Copilot/Codex/goose agents and instructions.
#   .github/workflows is never protected. On macOS it is NOT enforced (a warning; deferred).
#
# macOS AUGMENTATION (2026-W36) - added ONLY to the macOS (Darwin) branch. TWO DISTINCT mechanisms;
# do NOT conflate them (only group (i) is an actual Seatbelt/sandbox-exec feature):
#   (i)  SBPL / Seatbelt profile additions (the only real sandbox-exec expressions here):
#          - setuid-exec denylist:  (deny process-exec* (literal ...))   [best-effort, NOT exhaustive]
#          - egress deny / loopback-proxy allow rules
#   (ii) POSIX rlimits applied via `ulimit` BEFORE exec (KERNEL limits, NOT Seatbelt/SBPL features):
#          --cpu-max SEC  -> RLIMIT_CPU ;   --nproc-max N -> RLIMIT_NPROC
#   (iii) fail-honest, interface-only (enforces NOTHING on macOS):  --mem-max
# The Linux (bwrap) branch is unchanged; the three cap flags are no-ops there (Linux reaches CPU/PID/
# mem caps via cgroups on its OOB path). LINUX DELTA (for the parity test): these three flags were
# previously `unknown arg` -> exit 2; they now no-op-with-note -> exit 0.
#   --cpu-max SEC   (ii) RLIMIT_CPU: a per-PROCESS cpu-second cap - EACH descendant gets its OWN
#                   counter, so this is DoS-bounding, not a process-tree/aggregate quota. Aggregate/
#                   tree bounding needs --nproc-max under a dedicated uid, or cgroups on Linux. The
#                   process is terminated (SIGXCPU at the soft limit / SIGKILL at the hard limit, set
#                   equal) after SEC cpu-seconds. NOT a throttle or a fair-share quota.
#   --nproc-max N   (ii) RLIMIT_NPROC: bounds a *tenant* ONLY when the whole launcher is ALREADY
#                   running as a dedicated, operator-provisioned uid. On a shared uid RLIMIT_NPROC is
#                   per-UID and this flag is just a self-DoS knob, not isolation. The launcher does NOT
#                   drop uid (that would make it root-requiring - a rejected escalation surface). See
#                   dedicated-uid-provisioning.example.sh (inert, OOB).
#   --mem-max MiB   (iii) accepted for interface parity with Linux MemoryMax, but on macOS it does NOT
#                   cap memory. RLIMIT_AS/DATA/RSS are broken on arm64 and `taskpolicy -m` fires only
#                   under system memory pressure. The launcher prints a LOUD warning and PROCEEDS
#                   UNCAPPED. A hard memory cap requires a VM / container / Linux host (Layer B).
#
# DNS-THROUGH-PROXY CONTRACT (--egress proxy on macOS): SBPL has no hostname filter and its network
# address filter accepts ONLY host "*" or "localhost". `(deny network*)` blocks UDP/53 so the guest
# CANNOT self-resolve; only the loopback proxy port is opened. Therefore --proxy MUST be a loopback
# IP:PORT and the proxy MUST perform all name resolution on the guest's behalf. A remote proxy IP
# cannot be expressed in SBPL and FAILS CLOSED. Authoritative sole-proxy boundary is still OP1 (OOB).
#
# TIER C OMISSION (operator decision 2026-W36): NO syscall filtering is emitted. SBPL `syscall-unix`
# is undocumented and OS-/arch-version-gated; a curated set pins to one OS build. seccomp-grade policy
# = Linux host / Layer B. This launcher never emits `(deny syscall-*)` and never `(with no-sandbox)`.
# ============================================================================================
set -uo pipefail

SCRATCH=""; EGRESS="deny"; PROXY_ADDR="127.0.0.1"; PROXY_PORT="8443"; NETNS="agentteams-egress"
CHECK=0; EXCLUDES=(); WRITABLES=(); SETENVS=(); ENV_ALLOW=(); CMD=(); COORD_ROOTS=(); PROTECTS=()
# Project-relative control-plane paths (locked by a test to agentteams' _sandbox_emit
# protected_write_paths + governed_roster_paths + GRANT_ROSTER_PROJECT_REL, plus the goose profile).
# Protected wherever they exist under a writable root; see cp_required for when absence is a die.
CONTROL_PLANE_REL=( .claude/agents/references/agent-privilege.json .claude/hooks/constitutional-gate.py
                    .claude/agents/references/authorized-verify-keys
                    .claude/agents/references/security-approvers.txt .claude/agents/references/authorized-managers.txt
                    .claude/agents/references/management-authority.json
                    .goose/recipes/references/agent-privilege.json .goose/recipes/references/authorized-verify-keys
                    .goose/recipes/references/security-approvers.txt .goose/recipes/references/authorized-managers.txt
                    .goose/recipes/references/management-authority.json
                    .github/agents/references/agent-privilege.json .github/agents/references/authorized-verify-keys
                    .github/agents/references/security-approvers.txt .github/agents/references/authorized-managers.txt
                    .github/agents/references/management-authority.json
                    .codex/agents/references/agent-privilege.json .codex/agents/references/authorized-verify-keys
                    .codex/agents/references/security-approvers.txt .codex/agents/references/authorized-managers.txt
                    .codex/agents/references/management-authority.json .codex/config.toml
                    .goose/sandbox.sb references/security-approvers.txt .goose/confined-run.example.sh
                    .codex/confined-run.example.sh )
# Whole directories read-only wherever they exist under a writable root (follow-up #2, 2026-09-30):
# .claude holds the live settings.json whose allowWrite is the operator-accepted write baseline and
# the settings/hooks the next Claude session trusts. Mirrors Claude's own `.claude` denyWrite, so a
# confined goose/copilot/codex agent cannot rewrite them either. A mount point cannot be renamed.
CONTROL_PLANE_DIRS_REL=( .claude )
# Prompt roots (follow-up #8 phase 2), read-only only with --protect-prompt-roots, protect-if-present.
# Locked by a test to agentteams' _prompt_root_protect PROMPT_ROOT_FILES + PROMPT_ROOT_DIRS +
# PROMPT_ROOT_PRESENT_ONLY_DIRS. Never .github/workflows.
PROMPT_ROOTS_REL=( .github/copilot-instructions.md AGENTS.md AGENTS.override.md .goosehints CLAUDE.md CLAUDE.local.md .mcp.json
                   .github/instructions .github/prompts .github/agents .codex .goose/recipes .agentteams )
PROTECT_PROMPT_ROOTS=0; PR_RO=()
# The agentteams team marker, relative to an agents dir (locked to _sandbox_emit.TEAM_MARKER_REL).
TEAM_MARKER_REL=references/build-log.json
TEAM_DIRS_REL=( .claude/agents .goose/recipes .github/agents .codex/agents )
CP_ANC=(); CP_RO=(); CP_ROOTS=()
# DEFAULT-DENY ENV ALLOWLIST (the private-key non-leak residual). The guest inherits NONE of the
# launcher's environment by default: only these benign vars (when set) plus any --env-allow name and
# any explicit --setenv VAR=VAL are passed. Everything else - crucially an operator signing-key path
# or any *_SIGNING_KEY secret - is DROPPED, so it cannot leak into a confined agent. Unset-one-var
# would be fail-OPEN (you would have to know every secret name); default-deny is fail-closed.
DEFAULT_ENV_ALLOW=( PATH HOME USER LOGNAME TERM LANG LC_ALL LC_CTYPE LC_MESSAGES TZ TMPDIR SHELL )
# macOS-augmentation resource caps (empty = unset; validated numeric below). No-op on Linux.
CPU_MAX=""; NPROC_MAX=""; MEM_MAX=""

die(){ echo "confine-run: $*" >&2; exit 2; }

while [ $# -gt 0 ]; do
  case "$1" in
    --scratch) SCRATCH="${2:-}"; shift 2 ;;
    --egress)  EGRESS="${2:-}"; shift 2 ;;
    --proxy)   IFS=: read -r PROXY_ADDR PROXY_PORT <<<"${2:-}"; shift 2 ;;
    --netns)   NETNS="${2:-}"; shift 2 ;;
    --exclude) EXCLUDES+=("${2:-}"); shift 2 ;;
    --writable) WRITABLES+=("${2:-}"); shift 2 ;;
    --coord-root) COORD_ROOTS+=("${2:-}"); shift 2 ;;  # cross-repo coordination bind: FAIL-CLOSED if missing (never mkdir)
    --protect) PROTECTS+=("${2:-}"); shift 2 ;;  # extra read-only control-plane path: FAIL-CLOSED if missing (never mkdir)
    --setenv)  SETENVS+=("${2:-}"); shift 2 ;;
    --env-allow) ENV_ALLOW+=("${2:-}"); shift 2 ;;  # add a var NAME to the default-deny allowlist
    --cpu-max)  CPU_MAX="${2:-}";  shift 2 ;;   # macOS: RLIMIT_CPU (SEC cpu-seconds); no-op on Linux
    --nproc-max) NPROC_MAX="${2:-}"; shift 2 ;; # macOS: RLIMIT_NPROC (dedicated-uid only); no-op on Linux
    --mem-max)  MEM_MAX="${2:-}";  shift 2 ;;   # macOS: interface-only, UNCAPPED; no-op on Linux
    --protect-prompt-roots) PROTECT_PROMPT_ROOTS=1; shift ;;  # opt-in: ro-bind the present prompt roots (Linux)
    --check)   CHECK=1; shift ;;
    -h|--help) grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 0 ;;
    --) shift; CMD=("$@"); break ;;
    *) die "unknown arg: $1 (did you forget '--' before the command?)" ;;
  esac
done

# -- generic validation (OS-independent) ------------------------------------------------------
[ -n "$SCRATCH" ] || die "--scratch DIR is required (the only writable path inside the sandbox)"
[ -d "$SCRATCH" ] || die "--scratch '$SCRATCH' does not exist or is not a directory (fail-closed)"
[ "${#CMD[@]}" -gt 0 ] || die "no command given - put it after '--'"
case "$EGRESS" in deny|proxy|host) ;; *) die "--egress must be deny|proxy|host (got '$EGRESS')" ;; esac
# resource-cap args must be positive integers (also closes any injection into the ulimit sub-shell).
is_posint(){ case "$1" in ''|*[!0-9]*) return 1 ;; 0) return 1 ;; *) return 0 ;; esac; }
[ -n "$CPU_MAX" ]   && { is_posint "$CPU_MAX"   || die "--cpu-max expects a positive integer (cpu-seconds), got '$CPU_MAX'"; }
[ -n "$NPROC_MAX" ] && { is_posint "$NPROC_MAX" || die "--nproc-max expects a positive integer, got '$NPROC_MAX'"; }
[ -n "$MEM_MAX" ]   && { is_posint "$MEM_MAX"   || die "--mem-max expects a positive integer (MiB), got '$MEM_MAX'"; }
# proxy port must be a positive integer in range (interpolated verbatim into the SBPL profile).
if [ "$EGRESS" = proxy ]; then
  is_posint "$PROXY_PORT" && [ "$PROXY_PORT" -le 65535 ] || die "--proxy PORT must be an integer in 1..65535 (got '$PROXY_PORT')"
fi
SCRATCH="$(cd "$SCRATCH" && pwd)"

# cross-repo coordination binds: FAIL CLOSED if a declared sibling root is missing. Unlike
# --writable (which mkdir -p's a missing path), a coordination target that does not exist is a
# MISCONFIGURATION (a missing sibling repo) -- auto-creating an empty dir would mask it and hand
# the agent a bogus workspace, so we die instead. Checked HERE in the OS-independent block so a
# missing target is a clean die/exit-2 BEFORE OS dispatch -- never a bwrap init crash (D-3: on
# Linux `bwrap --bind SRC` on a missing SRC aborts sandbox init entirely; macOS tolerates it).
COORD_RESOLVED=()
for c in ${COORD_ROOTS[@]+"${COORD_ROOTS[@]}"}; do
  [ -n "$c" ] || continue
  [ -d "$c" ] || die "coordination target '$c' does not exist (fail-closed; not created -- a missing sibling repo is a misconfiguration, not something to auto-create)"
  COORD_RESOLVED+=( "$(cd "$c" && pwd)" )
done

# credential + caller read-excludes: only EXISTING paths (masking a missing path fails fail-shut: D-3).
# F-1: the operator signing-key dir is masked in every run; legacy key files (pre-keys/ layout) are
# masked one by one, as exact paths, until the operator migrates them (provision script --migrate).
MASK=( "$HOME/.ssh" "$HOME/.aws" "$HOME/.gnupg" "$HOME/.kube" "$HOME/.config/gcloud" "$HOME/.azure" )
MASK+=( "$HOME/.config/agentteams/keys" )
for p in "$HOME"/.config/agentteams/*.pem; do [ -f "$p" ] && MASK+=( "$p" ); done
MASK+=( ${EXCLUDES[@]+"${EXCLUDES[@]}"} )
MASKED=()
for p in "${MASK[@]}"; do [ -n "$p" ] && [ -e "$p" ] && MASKED+=( "$p" ); done
# ensure writable paths exist so the mount source is real
for w in ${WRITABLES[@]+"${WRITABLES[@]}"}; do [ -n "$w" ] && { mkdir -p "$w" 2>/dev/null || die "cannot create --writable '$w'"; }; done

# Combined env allowlist = the default benign set + any operator --env-allow additions. A name is
# passed to the guest ONLY if it appears here AND is set in the launcher's environment; --setenv
# VAR=VAL remains a separate, explicit value injection that always wins. Reject a malformed name so
# it cannot smuggle a value through the allowlist path (names only here; values come from the env).
ENV_ALLOW_ALL=( "${DEFAULT_ENV_ALLOW[@]}" ${ENV_ALLOW[@]+"${ENV_ALLOW[@]}"} )
for n in "${ENV_ALLOW_ALL[@]}"; do
  case "$n" in ''|*[!A-Za-z0-9_]*) die "--env-allow expects a bare VAR name (got '$n')" ;; esac
done

OS="$(uname -s)"

# ============================================================================================
# F-4 control plane -> CP_ANC[] (ancestor self-binds) + CP_RO[] (read-only binds), appended to BW[].
# GNU realpath (-e/-s/-m) on Linux; macOS's BSD realpath has none of those, so the macOS branch (bash 3.2
# compatible) resolves with `cd -P` and checks the leaf for a symlink itself (2026-10-07).
if realpath -e -- / >/dev/null 2>&1; then HAVE_GNU_REALPATH=1; else HAVE_GNU_REALPATH=0; fi
phys_dir(){   # existing directory -> its physical absolute path (every symlink resolved); nonzero when missing
  if [ "$HAVE_GNU_REALPATH" -eq 1 ]; then realpath -e -- "$1" 2>/dev/null; return; fi
  ( cd -P -- "$1" 2>/dev/null && pwd -P )
}
cp_real(){   # realpath of an existing path; die (in the $(...) subshell - callers then exit 2) when it
  # is missing, or is (or passes through) a symlink. Never creates anything.
  local r d n in="$1"
  while [ "${in%/}" != "$in" ] && [ "$in" != "/" ]; do in="${in%/}"; done   # a trailing / makes [ -L ] follow the link
  set -- "$in"
  if [ "$HAVE_GNU_REALPATH" -eq 1 ]; then
    r="$(realpath -e -- "$1" 2>/dev/null)" || die "control-plane path '$1' does not exist or does not resolve (fail-closed; never created)"
    [ "$r" = "$(realpath -s -m -- "$1")" ] || die "control-plane path '$1' is or passes through a symlink (resolves to '$r'); refusing (fail-closed)"
  else
    # Callers pass "<physical root>/<rel>", so the input is already its own logical form: any symlink on the
    # way (the leaf, or a directory under the root) makes the physical path differ from it.
    cp_present "$1" || die "control-plane path '$1' does not exist or does not resolve (fail-closed; never created)"
    [ -L "$1" ] && die "control-plane path '$1' is or passes through a symlink; refusing (fail-closed)"
    d="$(phys_dir "$(dirname -- "$1")")" || die "control-plane path '$1' does not exist or does not resolve (fail-closed; never created)"
    r="$d/$(basename -- "$1")"
    [ "$r" = "${1%/}" ] || die "control-plane path '$1' is or passes through a symlink (resolves to '$r'); refusing (fail-closed)"
  fi
  case "$r" in *$'\n'*) die "control-plane path contains a newline: $1" ;; esac
  # A protected regular file with a second hard link can be written through the alias, which no path-based
  # rule (Seatbelt) or bind of the original path (bwrap) covers. Refuse; the operator removes the extra link.
  if [ -f "$r" ]; then
    n="$(ls -ld -- "$r" 2>/dev/null | awk '{print $2}')"
    case "$n" in ''|*[!0-9]*) die "control-plane path '$r': cannot read its link count (fail-closed)" ;; esac
    [ "$n" -le 1 ] || die "control-plane path '$r' has $n hard links; an alias elsewhere could write it. Remove the extra link(s) from OUTSIDE the sandbox, then retry (fail-closed)"
  fi
  if [ -d "$r" ]; then   # the same for every file inside a protected directory (verify keys, .claude, ...)
    n="$(find "$r" -type f -links +1 -print 2>/dev/null | head -1)"
    [ -z "$n" ] || die "control-plane file '$n' (inside '$r') has more than one hard link; an alias elsewhere could write it. Remove the extra link(s) from OUTSIDE the sandbox, then retry (fail-closed)"
  fi
  printf '%s\n' "$r"
}
cp_present(){ [ -e "$1" ] || [ -L "$1" ]; }
cp_required(){   # root rel -> prints the owning agentteams team dir when rel MUST exist, else nothing
  local r="$1" rel="$2" team
  case "$rel" in
    .goose/sandbox.sb) return 0 ;;   # macOS-only artifact
    .codex/config.toml) return 0 ;;  # Codex's own config: protect-if-present (never stubbed)
    .goose/confined-run.example.sh) return 0 ;;  # operator-run example: protect-if-present
    .codex/confined-run.example.sh) return 0 ;;  # operator-run example: protect-if-present
    .claude/*) team="$r/.claude/agents" ;;
    .goose/*) team="$r/.goose/recipes" ;;
    .github/agents/*) team="$r/.github/agents" ;;   # never .github/* (workflows stay unprotected)
    .codex/agents/*) team="$r/.codex/agents" ;;
    *) return 0 ;;                   # project-root grant roster: protect-if-present
  esac
  cp_present "$team/$TEAM_MARKER_REL" || return 0   # not an agentteams team (e.g. hand-written)
  case "$rel" in
    */security-approvers.txt|*/authorized-managers.txt|*/management-authority.json)
      cp_present "$team/references/agent-privilege.json" || return 0 ;;   # rosters follow the switch
  esac
  printf '%s\n' "$team"
}
# DIAGNOSIS ONLY (message choice; the launcher refuses either way): an attacker who also plants one
# dummy agent file steers this to the generic "regenerate" hint. Nothing is granted.
team_looks_planted(){   # team dir -> true when it holds no agent file of its framework and no switch
  local t="$1" glob f
  case "$t" in
    */.claude/agents) glob="*.md" ;;
    */.goose/recipes) glob="*.yaml" ;;
    */.github/agents) glob="*.agent.md" ;;
    */.codex/agents) glob="*.toml" ;;
    *) return 1 ;;
  esac
  cp_present "$t/references/agent-privilege.json" && return 1
  while IFS= read -r f; do
    [ -n "$f" ] || continue
    case "${f##*/}" in SETUP-REQUIRED.md) continue ;; esac
    return 1
  done < <(compgen -G "$t/$glob" || true)
  return 0
}
regen_hint(){   # team dir -> how to regenerate it (MESSAGE ONLY; nothing is read or granted)
  case "$1" in
    */.codex/agents) printf '%s' "agentteams --update for a native Codex team; a Codex team written by an interop projection (origin: interop in $TEAM_MARKER_REL) is refreshed by re-running that projection OUTSIDE any agent sandbox: agentteams --interop-from <source> --framework codex --output . --overwrite" ;;
    *) printf '%s' "agentteams --update" ;;
  esac
}
# #11 (2026-09-30): `.codex/config.toml` is protect-if-present, so a file a confined process created
# is locked in from the next launch, and Codex run OUTSIDE this launcher would honour it. Warn on the
# security-relevant keys every run (key-based, never a digest an agent could re-record). Never a die.
# BEST-EFFORT: plain `key =` lines and `[table]` headers only; quoted keys, dotted keys
# (`mcp_servers.x.command =`), inline tables and `model_providers` base_url are not detected.
codex_config_warn(){
  local r f line keys=()
  for r in "$SCRATCH" ${WRITABLES[@]+"${WRITABLES[@]}"}; do
    f="$r/.codex/config.toml"
    if [ -L "$f" ]; then   # Codex outside the launcher follows the link: say so, never read it
      echo "confine-run: WARNING $(printf %q "$f") is a symlink; Codex run OUTSIDE this launcher reads its target. Review the target, and confirm you (not a confined process) created it." >&2
      continue
    fi
    [ -f "$f" ] || continue
    keys=()
    while IFS= read -r line || [ -n "$line" ]; do
      if [[ "$line" =~ ^[[:space:]]*(approval_policy|sandbox_mode|notify)[[:space:]]*= ]]; then keys+=( "${BASH_REMATCH[1]}" )
      elif [[ "$line" =~ ^[[:space:]]*\[(sandbox_workspace_write|mcp_servers)[].] ]]; then keys+=( "[${BASH_REMATCH[1]}]" )
      fi
    done < "$f"
    [ "${#keys[@]}" -gt 0 ] || continue
    echo "confine-run: WARNING $(printf %q "$f") sets security-relevant Codex keys (${keys[*]}). It is read-only in this sandbox, but Codex run OUTSIDE this launcher honours it: review it, and confirm you (not a confined process) wrote it." >&2
  done
}
control_plane_collect() {   # -> CP_RO[] (protected paths) + CP_ANC[] (their ancestors below a root); both OSes
  local roots=() prot=() anc=() r rel p a under t team
  for r in "$SCRATCH" ${WRITABLES[@]+"${WRITABLES[@]}"} ${COORD_RESOLVED[@]+"${COORD_RESOLVED[@]}"}; do
    [ -n "$r" ] && { p="$(phys_dir "$r")" || die "writable root '$r' does not resolve"; roots+=( "$p" ); }
  done
  for r in "${roots[@]}"; do
    for t in "${TEAM_DIRS_REL[@]}"; do   # the marker itself: deleting it must not disable the check
      cp_present "$r/$t/$TEAM_MARKER_REL" || continue
      p="$(cp_real "$r/$t/$TEAM_MARKER_REL")" || exit 2
      prot+=( "$p" )
    done
    for rel in "${CONTROL_PLANE_DIRS_REL[@]}"; do   # protect-if-present, whole dir
      cp_present "$r/$rel" || continue
      p="$(cp_real "$r/$rel")" || exit 2
      prot+=( "$p" )
    done
    if [ "$PROTECT_PROMPT_ROOTS" -eq 1 ]; then   # opt-in, protect-if-present (never required)
      for rel in "${PROMPT_ROOTS_REL[@]}"; do
        cp_present "$r/$rel" || continue
        p="$(cp_real "$r/$rel")" || exit 2
        prot+=( "$p" ); PR_RO+=( "$p" )
      done
    fi
    for rel in "${CONTROL_PLANE_REL[@]}"; do
      if ! cp_present "$r/$rel"; then
        # Absent. A hole when the entry is REQUIRED (cp_required): its parent is rename-locked yet
        # WRITABLE, so a confined process could create a `false` switch, a verify-key store with a
        # planted .pub.pem, a gate hook or a roster naming itself. Refuse (never create).
        team="$(cp_required "$r" "$rel")"
        [ -n "$team" ] || continue
        if team_looks_planted "$team"; then
          die "control-plane path $(printf %q "$r/$rel") is missing although the agentteams team $(printf %q "$team") exists, but it holds only an agentteams marker ($TEAM_MARKER_REL) and no agent files: it may have been PLANTED by a confined process. If you did not generate an agentteams team there, inspect and remove $(printf %q "$team/$TEAM_MARKER_REL") from OUTSIDE the sandbox, then retry. Otherwise regenerate the team ($(regen_hint "$team")). Nothing was changed (fail-closed)."
        fi
        die "control-plane path $(printf %q "$r/$rel") is missing although the agentteams team $(printf %q "$team") exists: a confined process could create it (fail-closed; never created). Regenerate the team with current agentteams ($(regen_hint "$team")) so it is emitted (agentteams before 2026-09-30 did not emit it for every framework and platform), then retry."
      fi
      p="$(cp_real "$r/$rel")" || exit 2
      prot+=( "$p" )
    done
  done
  for p in ${PROTECTS[@]+"${PROTECTS[@]}"}; do
    [ -n "$p" ] || continue
    a="$(cp_real "$p")" || exit 2   # a missing --protect path is a die, never a mkdir
    prot+=( "$a" )
  done
  CP_ROOTS=( ${roots[@]+"${roots[@]}"} )
  [ "${#prot[@]}" -gt 0 ] || return 0
  for p in "${prot[@]}"; do   # every ancestor strictly below a writable root
    a="$(dirname -- "$p")"
    while :; do
      under=0; for r in "${roots[@]}"; do case "$a" in "$r"/*) under=1 ;; esac; done
      [ "$under" -eq 1 ] || break
      anc+=( "$a" ); a="$(dirname -- "$a")"
    done
  done
  # a parent sorts before its children (a prefix sorts first), so the self-binds go top-down.
  # `while read` rather than mapfile: the macOS branch must run under /bin/bash 3.2.
  CP_ANC=(); CP_RO=()
  if [ "${#anc[@]}" -gt 0 ]; then
    while IFS= read -r a; do CP_ANC+=( "$a" ); done < <(printf '%s\n' "${anc[@]}" | LC_ALL=C sort -u)
  fi
  while IFS= read -r p; do CP_RO+=( "$p" ); done < <(printf '%s\n' "${prot[@]}" | LC_ALL=C sort -u)
}
control_plane_binds() {   # Linux: rename-lock ancestors with self-binds, then read-only binds
  control_plane_collect
  local a p
  for a in ${CP_ANC[@]+"${CP_ANC[@]}"}; do BW+=( --bind "$a" "$a" ); done
  for p in ${CP_RO[@]+"${CP_RO[@]}"}; do BW+=( --ro-bind "$p" "$p" ); done
}

# ============================================================================================
build_linux() {   # -> RUN[] using bwrap
  command -v bwrap >/dev/null 2>&1 || die "bwrap (bubblewrap) not found - install: sudo apt-get install -y bubblewrap"
  # macOS-augmentation resource-cap flags are NO-OPS on Linux (degrade safely): Linux reaches CPU/
  # PID/memory caps through cgroups on its OOB netns/systemd path, not through these flags.
  # LINUX DELTA (parity test): these flags used to be an `unknown arg` hard-fail (exit 2); now a no-op.
  if [ -n "$CPU_MAX$NPROC_MAX$MEM_MAX" ]; then
    echo "confine-run: note - --cpu-max/--nproc-max/--mem-max are macOS-branch flags; ignored on Linux (use cgroups OOB)." >&2
  fi
  # --clearenv makes the guest env default-DENY: bwrap otherwise inherits the launcher's full parent
  # environment (there is no implicit scrub), so a signing-key path or *_SIGNING_KEY secret would
  # leak straight through. We clear it, then add back ONLY the allowlist + explicit --setenv below.
  local BW=( bwrap --clearenv --ro-bind / / --tmpfs /tmp --dev /dev --proc /proc
                   --bind "$SCRATCH" "$SCRATCH" --chdir "$SCRATCH"
                   --die-with-parent --new-session
                   --unshare-user --unshare-ipc --unshare-pid --unshare-uts --unshare-cgroup )
  local w; for w in ${WRITABLES[@]+"${WRITABLES[@]}"}; do [ -n "$w" ] && BW+=( --bind "$w" "$w" ); done
  local c; for c in ${COORD_RESOLVED[@]+"${COORD_RESOLVED[@]}"}; do BW+=( --bind "$c" "$c" ); done  # cross-repo coordination (existence pre-verified -> no bwrap init crash)
  control_plane_binds   # F-4: AFTER the rw roots, BEFORE the masks (see CONTROL PLANE above)
  # allowlist passthrough first (default-deny env), then explicit --setenv so an explicit value wins.
  local n; for n in "${ENV_ALLOW_ALL[@]}"; do [ -n "${!n+x}" ] && BW+=( --setenv "$n" "${!n}" ); done
  local kv; for kv in ${SETENVS[@]+"${SETENVS[@]}"}; do [ -n "$kv" ] && { case "$kv" in *=*) BW+=( --setenv "${kv%%=*}" "${kv#*=}" ) ;; *) die "--setenv expects VAR=VAL (got '$kv')" ;; esac; }; done
  # a directory is hidden under an empty tmpfs; a FILE cannot take a tmpfs mount (bwrap aborts), so
  # it is shadowed by a read-only bind of /dev/null instead.
  local m; for m in ${MASKED[@]+"${MASKED[@]}"}; do
    if [ -d "$m" ]; then BW+=( --tmpfs "$m" ); else BW+=( --ro-bind /dev/null "$m" ); fi
  done
  case "$EGRESS" in
    deny) BW+=( --unshare-net ); RUN=( "${BW[@]}" -- "${CMD[@]}" ) ;;
    host) echo "confine-run: WARNING --egress host - network SHARED with host; egress NOT confined (fs/read/NNP still apply)." >&2
          RUN=( "${BW[@]}" -- "${CMD[@]}" ) ;;
    proxy) command -v ip >/dev/null 2>&1 || die "--egress proxy needs iproute2 (ip)"
           ip netns list 2>/dev/null | grep -qw "$NETNS" || die "--egress proxy requires netns '$NETNS' to already exist (apply as root via egress-netns-wiring.sh --apply, then re-run). [OPERATOR-OOB]"
           RUN=( ip netns exec "$NETNS" "${BW[@]}" -- "${CMD[@]}" ) ;;
  esac
}

# ============================================================================================
# Reject any path that would be interpolated verbatim into the generated SBPL profile if it contains
# a double-quote, a backslash, or a newline - any of these can break out of the `(subpath "...")`
# string and inject arbitrary SBPL directives, widening the profile (SECURITY C1). A backslash is the
# SBPL/string escape char and can escape the closing quote even when no literal double-quote is
# present (agentteams @security 2026-W36 - closed a residual the quote/newline check missed). Applied
# to $SCRATCH, every resolved --writable path, and every masked credential/--exclude path. macOS-only
# (SBPL is macOS-only), so the Linux branch keeps its exact prior behavior.
reject_sbpl_meta(){
  case "$1" in
    *\\*)    die "path contains a backslash, which could escape the SBPL string quote (fail-closed): $1" ;;
    *'"'*)   die "path contains a double-quote, which could inject SBPL directives (fail-closed): $1" ;;
    *$'\n'*) die "path contains a newline, which could inject SBPL directives (fail-closed): $1" ;;
  esac
}

# ============================================================================================
build_macos() {   # -> RUN[] using sandbox-exec + a generated path-agnostic Seatbelt profile
  command -v sandbox-exec >/dev/null 2>&1 || die "sandbox-exec not found (macOS only)"
  local sb="$SCRATCH/.confine.sandbox.sb"
  # -- proxy egress: SBPL network address filters accept ONLY host "*" or "localhost" (verified on
  # 26.5.2 arm64: `(remote ip "<any-real-IP>:port")` fails at PARSE -> "host must be * or localhost").
  # So macOS can pin sole-proxy egress ONLY to a loopback proxy. A remote proxy IP cannot be expressed;
  # we FAIL-HONEST (die) rather than silently widen to `*:port` (which would NOT be sole-proxy).
  # (::1 is intentionally NOT accepted: `IFS=: read` splits it away, and IPv6 loopback is not needed.)
  if [ "$EGRESS" = proxy ]; then
    case "$PROXY_ADDR" in
      127.0.0.1|localhost) : ;;   # loopback proxy - expressible as (remote ip "localhost:PORT")
      *) die "--egress proxy: macOS Seatbelt cannot pin egress to a remote proxy IP ('$PROXY_ADDR'); \
SBPL only allows host '*' or 'localhost'. Run the proxy on loopback (127.0.0.1 - e.g. an ssh -L / \
socat forward) OR use the OOB dedicated-uid + PF-per-tenant path. FAIL CLOSED." ;;
    esac
  fi
  # SECURITY C1: validate every path that gets interpolated into the profile BEFORE it is written.
  reject_sbpl_meta "$SCRATCH"
  local w; for w in ${WRITABLES[@]+"${WRITABLES[@]}"}; do [ -n "$w" ] && reject_sbpl_meta "$(cd "$w" && pwd)"; done
  local c; for c in ${COORD_RESOLVED[@]+"${COORD_RESOLVED[@]}"}; do reject_sbpl_meta "$c"; done
  local m; for m in ${MASKED[@]+"${MASKED[@]}"}; do reject_sbpl_meta "$m"; done
  # F-4 on macOS (2026-10-07): the same control-plane set the Linux branch ro-binds, from the same collector.
  control_plane_collect
  local cp; for cp in ${CP_RO[@]+"${CP_RO[@]}"} ${CP_ANC[@]+"${CP_ANC[@]}"} ${CP_ROOTS[@]+"${CP_ROOTS[@]}"}; do reject_sbpl_meta "$cp"; done
  {
    echo '(version 1)'
    echo '(allow default)'
    echo '(deny file-write*)'
    echo "(allow file-write* (subpath \"$SCRATCH\"))"
    echo '(allow file-write* (subpath "/private/tmp") (subpath "/private/var/folders") (literal "/dev/null") (literal "/dev/stdout") (literal "/dev/stderr"))'
    for w in ${WRITABLES[@]+"${WRITABLES[@]}"}; do [ -n "$w" ] && echo "(allow file-write* (subpath \"$(cd "$w" && pwd)\"))"; done
    for c in ${COORD_RESOLVED[@]+"${COORD_RESOLVED[@]}"}; do echo "(allow file-write* (subpath \"$c\"))"; done
    # Control plane, AFTER the allows (in SBPL the last matching rule wins): each protected path is
    # write-denied as a subpath, and each ancestor below a writable root is write-denied as a literal, so it
    # can't be renamed or removed to move the protected path away, while files can still be created in it.
    for cp in ${CP_RO[@]+"${CP_RO[@]}"}; do echo "(deny file-write* (subpath \"$cp\"))"; done
    for cp in ${CP_ANC[@]+"${CP_ANC[@]}"}; do echo "(deny file-write* (literal \"$cp\"))"; done
    # Rename-lock every writable root and all its ancestors too: under an allowed subpath (/private/tmp,
    # /private/var/folders) a root could otherwise be renamed away, its control plane written at the new
    # path, and renamed back (a path-based deny follows the path, not the file). bwrap roots are mount points.
    if [ "${#CP_RO[@]}" -gt 0 ]; then
      for cp in ${CP_ROOTS[@]+"${CP_ROOTS[@]}"}; do
        while [ -n "$cp" ] && [ "$cp" != "/" ]; do echo "(deny file-write* (literal \"$cp\"))"; cp="$(dirname -- "$cp")"; done
      done
    fi
    for m in ${MASKED[@]+"${MASKED[@]}"}; do echo "(deny file-read* (subpath \"$m\"))"; done
    # -- (i) SBPL setuid/setgid-exec restriction (compensating hardening, NOT a no-new-privs guarantee) --
    # SBPL cannot express the setuid BIT itself, so this is a BEST-EFFORT, NOT-EXHAUSTIVE denylist of
    # the known macOS system setuid-/setgid-root escalation binaries, denied via
    # `(deny process-exec* (literal ...))`.
    # OOB RECONCILIATION: enumerate the box's actual setuid/setgid set and reconcile this list with:
    #     find / -perm -4000 -o -perm -2000  2>/dev/null
    # HONEST CEILING: (1) this is NOT `no-new-privs` - it only blocks these specific exec targets;
    # (2) the list is best-effort and NOT exhaustive - a setuid binary not listed here is not blocked;
    # (3) literal-path matching may be bypassable by path aliasing (symlink/hardlink) - the deny test
    #     (mac-escape-tests.sh gates H2) probes this; if a bypass is found the label downgrades to
    #     "blocks only direct literal-path invocation";
    # (4) it does NOT cover an arbitrary attacker-supplied setuid file - but a file copied into the
    #     writable scratch cannot become setuid-ROOT unprivileged (no chown-to-root), so the real
    #     escalation vector is exec of the pre-existing system setuid-root binaries below;
    # (5) we NEVER emit `(with no-sandbox)` (rejected by SBPL for deny anyway, and an escape hatch by
    #     design). Add paths here rather than widening to a `(with no-sandbox)` allow.
    local suid; for suid in \
        /usr/bin/sudo /usr/bin/su /usr/bin/login /usr/bin/newgrp /usr/bin/passwd \
        /usr/bin/crontab /usr/bin/at /usr/bin/atq /usr/bin/atrm /usr/bin/batch \
        /usr/bin/quota /usr/libexec/authopen /usr/libexec/security_authtrampoline \
        /usr/sbin/traceroute /usr/sbin/traceroute6 ; do
      echo "(deny process-exec* (literal \"$suid\"))"
    done
    case "$EGRESS" in
      deny) echo '(deny network*)' ;;   # also blocks UDP/53 -> guest cannot self-resolve DNS
      host) : ;;  # network stays allowed by (allow default)
      proxy) # DNS-THROUGH-PROXY CONTRACT: `(deny network*)` blocks UDP/53 so the guest cannot
             # self-resolve; ONLY the loopback proxy port is opened (host pinned to "localhost" - the
             # only non-"*" host SBPL accepts). The proxy MUST run on loopback and MUST do all name
             # resolution. Authoritative sole-proxy boundary is OP1 (OOB).
             echo '(deny network*)'; echo "(allow network* (remote ip \"localhost:$PROXY_PORT\"))"
             echo "; NOTE: SBPL host filter is limited to '*'/'localhost'; sole-proxy egress is pinned to"
             echo ";       the loopback proxy port only, and the proxy performs all DNS. Boundary = OP1 (OOB)." ;;
    esac
  } > "$sb"
  local PREFIX=()
  local kv; for kv in ${SETENVS[@]+"${SETENVS[@]}"}; do [ -n "$kv" ] && { case "$kv" in *=*) PREFIX+=( "$kv" ) ;; *) die "--setenv expects VAR=VAL (got '$kv')" ;; esac; }; done
  # DEFAULT-DENY env via `env -i`: start from an EMPTY environment (Seatbelt does not scrub env), add
  # back ONLY the allowlist (when set) then the explicit --setenv values (which win). Without -i the
  # guest would inherit the launcher's full env, leaking a signing-key path / *_SIGNING_KEY secret.
  local ENVI=( env -i )
  local n; for n in "${ENV_ALLOW_ALL[@]}"; do [ -n "${!n+x}" ] && ENVI+=( "$n=${!n}" ); done
  # inner command = env -i (allowlist) + (optional explicit setenv) + sandbox-exec on the profile
  local INNER=( "${ENVI[@]}" ${PREFIX[@]+"${PREFIX[@]}"} sandbox-exec -f "$sb" "${CMD[@]}" )
  # -- (ii) POSIX rlimits via ulimit (KERNEL, not Seatbelt), applied to the launcher process and
  # INHERITED by the guest across exec (an unprivileged guest cannot raise them). Wrapped in a tiny
  # sub-shell so the effective RUN[] is honest/visible in --check and self-contained.
  local ULIM=""
  if [ -n "$CPU_MAX" ]; then
    # RLIMIT_CPU: per-PROCESS cpu-second cap (each descendant gets its own counter). SIGXCPU at the
    # soft limit (default action: terminate); SIGKILL at the hard limit. `ulimit -t` sets both equal.
    ULIM+="ulimit -t $CPU_MAX; "
  fi
  if [ -n "$NPROC_MAX" ]; then
    # RLIMIT_NPROC is PER-UID. This isolates a tenant ONLY when confine-run.sh is ALREADY running as a
    # dedicated, operator-provisioned uid (see dedicated-uid-provisioning.example.sh). On a shared
    # login uid it counts ALL the user's processes -> a self-DoS knob, NOT isolation. The launcher
    # deliberately does NOT drop uid (no sudo/launchctl - that would make it root-requiring and an
    # argv-fed escalation surface). Provisioning the uid is OOB.
    echo "confine-run: WARNING --nproc-max only isolates a tenant under a DEDICATED uid (operator-provisioned); on a shared uid it is a self-DoS knob, not isolation." >&2
    ULIM+="ulimit -u $NPROC_MAX; "
  fi
  if [ -n "$ULIM" ]; then RUN=( bash -c "${ULIM}exec \"\$@\"" _ "${INNER[@]}" ); else RUN=( "${INNER[@]}" ); fi
  # -- (iii) memory is fail-honest. Accept --mem-max for interface parity, but do NOT claim a cap.
  if [ -n "$MEM_MAX" ]; then
    echo "confine-run: WARNING!! MEMORY UNCAPPED on macOS - --mem-max ${MEM_MAX}MiB is NOT enforced." >&2
    echo "confine-run:    (RLIMIT_AS/DATA/RSS broken on arm64; taskpolicy fires only under pressure.)" >&2
    echo "confine-run:    A hard memory cap requires a VM / container / Linux host (Layer B). Proceeding UNCAPPED." >&2
  fi
  [ "$EGRESS" = host ] && echo "confine-run: WARNING --egress host - network NOT confined (fs/read still apply)." >&2
  echo "confine-run: WARNING macOS Seatbelt path is ENFORCEMENT-UNVERIFIED until an on-mac deny test passes." >&2
}

case "$OS" in
  Linux)  build_linux ;;
  Darwin) build_macos ;;
  *) die "unsupported OS '$OS' - confinement is Linux (bwrap) or macOS (sandbox-exec) only. FAIL CLOSED." ;;
esac

codex_config_warn
if [ "$CHECK" -eq 1 ]; then
  echo "== confine-run --check (inert; nothing runs) =="
  echo "  os                : $OS"
  echo "  scratch (writable): $SCRATCH"
  if [ "$EGRESS" = proxy ] && [ "$OS" = Darwin ]; then
    # macOS emits the loopback form regardless of PROXY_ADDR (validated to loopback above).
    echo "  egress mode       : proxy  (macOS emits: (allow network* (remote ip \"localhost:$PROXY_PORT\")))"
  elif [ "$EGRESS" = proxy ]; then
    echo "  egress mode       : proxy  (netns=$NETNS, proxy=$PROXY_ADDR:$PROXY_PORT)"
  else
    echo "  egress mode       : $EGRESS"
  fi
  echo "  read-excluded     : ${MASKED[*]:-<none present>}"
  echo "  control-plane (ro): ${CP_RO[*]:-<none>}$( [ "${#CP_ANC[@]}" -gt 0 ] && echo " (rename-locked ancestors: ${CP_ANC[*]})" )"
  [ "$PROTECT_PROMPT_ROOTS" -eq 1 ] && echo "  prompt-roots (ro) : ${PR_RO[*]:-<none present>}"
  echo "  coord-roots       : ${COORD_RESOLVED[*]:-<none>}$( [ "${#COORD_RESOLVED[@]}" -gt 0 ] && echo " (cross-repo binds; existence pre-verified, fail-closed if missing)" )"
  echo "  env allowlist     : ${ENV_ALLOW_ALL[*]} (default-deny; all other env vars dropped)"
  echo "  cpu-max (RLIMIT)  : ${CPU_MAX:-<none>}$( [ -n "$CPU_MAX" ] && echo " cpu-sec (POSIX RLIMIT_CPU, per-process, kernel-enforced, DoS-bound)" )"
  echo "  nproc-max (RLIMIT): ${NPROC_MAX:-<none>}$( [ -n "$NPROC_MAX" ] && echo " (POSIX RLIMIT_NPROC, per-uid; isolates only under a dedicated uid)" )"
  echo "  mem-max           : ${MEM_MAX:-<none>}$( [ -n "$MEM_MAX" ] && echo " MiB requested - UNCAPPED on macOS (interface-only, fail-honest)" )"
  echo "  command           : ${CMD[*]}"
  echo "  effective         : ${RUN[*]}"
  exit 0
fi

exec "${RUN[@]}"
