# Linux Security Hardening — LearnPythonStatsEcon

<!--
SECTION MANIFEST — security-linux-hardening.reference.template.md
| section_id       | designation   | notes                                              |
|------------------|---------------|----------------------------------------------------|
| linux_hardening  | FENCED        | Curated Linux hardening baseline + verified sources |
-->

Platform-specific hardening baseline for `@security` when a project **builds,
deploys, or executes on Linux** — containers, servers, native binaries, kernel
or driver code. It is the systems-tier companion to the low-level / memory-safety
screening in `.github/agents/security.agent.md` (the "Low-Level & Systems
Vulnerabilities" block): that block screens *code*; this reference screens the
*platform* the code runs on. Parallel in structure to the macOS and Windows
hardening references.

This is a **curated baseline of authoritative guidance**, not a live threat feed
(that is `references/security-vulnerability-watch.reference.md`). Every source in
the registry is a primary, reputable authority — kernel.org and the Linux
man-pages project, NSA/CISA, NIST/MITRE, CIS, and the relevant OS/tooling projects
(SELinux, AppArmor, systemd, Debian, OpenSSF, OpenSCAP, CISOfy). Per Rule S-3
(Reference Integrity), do not add a source here without verifying it resolves to
the named authority.

<!-- AGENTTEAMS:BEGIN linux_hardening v=1 -->
## How `@security` uses this reference

- **Scope gate:** consult this reference only for Linux/native deployment targets.
  For a pure managed-runtime app that never touches Linux specifics, it does not apply.
- **Screen, don't remediate:** `@security` is read-only. Flag an unmet control as a
  finding and route remediation to the owning agent; escalate exploitation-likely
  gaps to `@orchestrator` with a HALT recommendation.
- **Tie to the code tier:** platform gaps here compound the code-level classes
  (out-of-bounds write CWE-787, use-after-free CWE-416, command injection CWE-78).
  A memory-safety bug behind a hardened kernel + seccomp + MAC profile is far less
  exploitable than the same bug on a permissive host.

## 1. System integrity, kernel & secure boot

Reduce kernel attack surface and enable self-protection so a memory bug in one
subsystem cannot trivially escalate. Key controls: enable KSPP-recommended build
options; restrict kernel pointer exposure (`kernel.kptr_restrict=2`), dmesg
(`kernel.dmesg_restrict=1`), unprivileged BPF (`kernel.unprivileged_bpf_disabled=1`),
`kernel.yama.ptrace_scope`; enforce module signing; keep KASLR enabled; minimize
loadable modules and built-in attack surface.

- Kernel Self-Protection — kernel.org — <https://docs.kernel.org/security/self-protection.html>
- Kernel Self Protection Project (KSPP) — Linux Foundation community — <https://kspp.github.io/>
- Documentation for `/proc/sys/kernel/` sysctls — kernel.org — <https://docs.kernel.org/admin-guide/sysctl/kernel.html>

## 2. Privilege-escalation vectors & privilege model

Where a local unprivileged user becomes root. Minimize SUID/SGID binaries (audit
with `find / -perm /6000`); keep `sudo` patched and least-privilege (no unbounded
`NOPASSWD`, no wildcard commands); enforce a secure `secure_path`; remove
world-writable files and writable entries on `PATH`; scope file capabilities
(`getcap -r /`). Landmark local-root CVEs: **PwnKit** (polkit `pkexec`,
CVE-2021-4034) and **Baron Samedit** (sudo, CVE-2021-3156).

- credentials(7) — Linux man-pages — <https://man7.org/linux/man-pages/man7/credentials.7.html>
- Privilege Escalation, Tactic TA0004 (Enterprise, incl. Linux) — MITRE ATT&CK — <https://attack.mitre.org/tactics/TA0004/>
- Sudo Security Advisories — sudo project (Todd C. Miller) — <https://www.sudo.ws/security/advisories/>

## 3. Mandatory access control / application control

Confine services so a compromised process cannot exceed a declared policy —
defense-in-depth beyond discretionary Unix permissions. Run SELinux
**enforcing** (not permissive/disabled) with a targeted-or-stricter policy, or
load AppArmor profiles for every network-facing service. Treat "set the whole
service unconfined / permissive" as a finding.

- The SELinux Project (upstream) — <https://selinuxproject.github.io/>
- selinux(8) — Linux man-pages — <https://man7.org/linux/man-pages/man8/selinux.8.html>
- AppArmor documentation — AppArmor project — <https://apparmor.net/>

## 4. Application isolation, sandboxing & containers

Containers are namespaces + cgroups + capabilities + seccomp + MAC — not a
security boundary by themselves. Drop all capabilities and add back only what is
needed (`--cap-drop=ALL`), run non-root, set `no-new-privileges`, use read-only
root filesystems, apply a seccomp + AppArmor/SELinux profile, and never mount the
Docker/host socket or run `--privileged` in reachable workloads. Canonical
container escape: **runc** `/proc/self/exe` overwrite (CVE-2019-5736).

- namespaces(7) — Linux man-pages — <https://man7.org/linux/man-pages/man7/namespaces.7.html>
- cgroups(7) — Linux man-pages — <https://man7.org/linux/man-pages/man7/cgroups.7.html>
- Kubernetes Hardening Guidance — NSA / CISA — <https://www.cisa.gov/news-events/alerts/2022/03/15/updated-kubernetes-hardening-guide>
- CVE-2019-5736 (runc container escape) — NIST NVD — <https://nvd.nist.gov/vuln/detail/CVE-2019-5736>

## 5. Capability & process-mitigation restriction

Shrink the syscall and privilege surface a process can reach. Apply a seccomp-BPF
allowlist (default-deny) to sandbox untrusted or network-facing code; split root
with capabilities(7) rather than running full-root; set `NoNewPrivileges` so
SUID/file-caps cannot re-expand privileges after a drop.

- seccomp(2) — Linux man-pages — <https://man7.org/linux/man-pages/man2/seccomp.2.html>
- capabilities(7) — Linux man-pages — <https://man7.org/linux/man-pages/man7/capabilities.7.html>
- Seccomp BPF (kernel filter semantics) — kernel.org — <https://docs.kernel.org/userspace-api/seccomp_filter.html>

## 6. Userspace memory-protection & exploit mitigations

Compile-and-link so that the memory-safety defects screened in the low-level code
block are harder to weaponize. Require: ASLR (system-wide `randomize_va_space=2`),
NX/DEP, stack canaries (`-fstack-protector-strong`), `-D_FORTIFY_SOURCE=2/3`,
full RELRO + BIND_NOW (`-Wl,-z,relro,-z,now`), position-independent executables
(`-fPIE -pie`), and CET/branch-protection where the toolchain and CPU support it
(`-D_FORTIFY_SOURCE=3` on GCC 12+/Clang 9+; fall back to `=2`). Treat a shipped
native binary missing these as a finding.

- Compiler Options Hardening Guide for C and C++ (`_FORTIFY_SOURCE=3`, stack protector, RELRO, PIE, CET) — OpenSSF — <https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html>
- Hardening (stack protector, FORTIFY_SOURCE, PIE, RELRO, format-string) — Debian project — <https://wiki.debian.org/Hardening>

## 7. Service / daemon hardening

Every long-running service should declare a sandbox in its unit. High-value
directives: `NoNewPrivileges=yes`, `ProtectSystem=strict`, `ProtectHome=yes`,
`PrivateTmp=yes`, `PrivateDevices=yes`, `ProtectKernelModules/Tunables/Logs=yes`,
`RestrictAddressFamilies=`, `CapabilityBoundingSet=`, `SystemCallFilter=`.
Score every unit with `systemd-analyze security` (0.0–10.0 exposure) and drive it
down. An unsandboxed network-facing unit is a finding.

- systemd.exec(5) — sandboxing directives — freedesktop.org (systemd) — <https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html>
- systemd-analyze (`security` verb) — Linux man-pages — <https://man7.org/linux/man-pages/man1/systemd-analyze.1.html>

## 8. Filesystem, disk encryption & secrets at rest

Partition and mount with intent: `nodev,nosuid,noexec` on `/tmp`, `/var/tmp`,
`/dev/shm` and removable media; separate `/var`, `/var/log`, `/home`. Remove
unneeded SUID/SGID bits. Keep secrets out of world-readable files, process
environments, and images; prefer a secrets manager or `0600` root-owned files;
enable disk encryption for data at rest. Use CIS + SCAP content as the concrete
control catalog.

- CIS Distribution-Independent Linux Benchmark (NIST National Checklist 1129) — NIST/CIS — <https://ncp.nist.gov/checklist/1129>
- CIS Benchmarks (all platforms) — Center for Internet Security — <https://www.cisecurity.org/cis-benchmarks/>
- OpenSCAP (SCAP 1.2 scanning toolkit) — OpenSCAP project — <https://www.open-scap.org/>

## 9. Auditing, detection & compliance

Make hardening measurable and continuous. Run `auditd` with a rule set covering
privileged syscalls, identity/auth files, and SUID execution; scan against a SCAP
Security Guide (SSG) profile with OpenSCAP; run `lynis audit system` for a broad
host baseline; track drift against a CIS Benchmark over time.

- auditd(8) — Linux Audit — <https://man7.org/linux/man-pages/man8/auditd.8.html>
- ComplianceAsCode / SCAP Security Guide (SSG profiles) — Red Hat / community — <https://github.com/ComplianceAsCode/content>
- Lynis — host security auditing — CISOfy — <https://cisofy.com/lynis/>

## 10. Vulnerability & exploit-class catalogs (cross-cutting)

Anchor findings to authoritative catalogs so they are reproducible and rateable.

- Common Weakness Enumeration (CWE) — MITRE (CISA-sponsored) — <https://cwe.mitre.org/>
- MITRE ATT&CK (Enterprise / Linux TTPs) — MITRE — <https://attack.mitre.org/>
- Known Exploited Vulnerabilities (KEV) Catalog — CISA — <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- National Vulnerability Database (CVE / CVSS / CPE) — NIST — <https://nvd.nist.gov/>

## Landmark Linux privilege-escalation / kernel exploits (illustrative)

Concrete exploit classes to recognize; each links to its NVD entry.

- **Dirty COW** (CVE-2016-5195) — COW race in `mm/gup.c` → write to read-only mappings → root — <https://nvd.nist.gov/vuln/detail/CVE-2016-5195>
- **Dirty Pipe** (CVE-2022-0847) — uninitialized pipe-buffer flags overwrite read-only file pages → priv-esc — <https://nvd.nist.gov/vuln/detail/CVE-2022-0847>
- **runc container escape** (CVE-2019-5736) — `/proc/self/exe` FD mishandling overwrites host `runc` → host root — <https://nvd.nist.gov/vuln/detail/CVE-2019-5736>
- **Baron Samedit** (CVE-2021-3156) — heap overflow in `sudo` via `sudoedit -s` trailing backslash → root — <https://nvd.nist.gov/vuln/detail/CVE-2021-3156>
- **PwnKit** (CVE-2021-4034) — polkit `pkexec` argv mishandling runs attacker env → local root — <https://nvd.nist.gov/vuln/detail/CVE-2021-4034>

## Source registry (authoritative, verified)

All URLs point to a primary authority. Government/official hosts that block
automated fetchers (cisa.gov, freedesktop.org/systemd, sudo.ws, cisecurity.org)
are cited at their canonical location and load normally in a browser.

| Domain | Source | Publisher | URL |
|---|---|---|---|
| Kernel | Kernel Self-Protection | kernel.org | <https://docs.kernel.org/security/self-protection.html> |
| Kernel | KSPP | Linux Foundation | <https://kspp.github.io/> |
| Kernel | kernel sysctls | kernel.org | <https://docs.kernel.org/admin-guide/sysctl/kernel.html> |
| Priv-esc | credentials(7) | Linux man-pages | <https://man7.org/linux/man-pages/man7/credentials.7.html> |
| Priv-esc | ATT&CK TA0004 | MITRE | <https://attack.mitre.org/tactics/TA0004/> |
| Priv-esc | sudo advisories | sudo project | <https://www.sudo.ws/security/advisories/> |
| MAC/LSM | SELinux Project | SELinux upstream | <https://selinuxproject.github.io/> |
| MAC/LSM | selinux(8) | Linux man-pages | <https://man7.org/linux/man-pages/man8/selinux.8.html> |
| MAC/LSM | AppArmor | AppArmor project | <https://apparmor.net/> |
| Containers | namespaces(7) | Linux man-pages | <https://man7.org/linux/man-pages/man7/namespaces.7.html> |
| Containers | cgroups(7) | Linux man-pages | <https://man7.org/linux/man-pages/man7/cgroups.7.html> |
| Containers | Kubernetes Hardening | NSA/CISA | <https://www.cisa.gov/news-events/alerts/2022/03/15/updated-kubernetes-hardening-guide> |
| seccomp | seccomp(2) | Linux man-pages | <https://man7.org/linux/man-pages/man2/seccomp.2.html> |
| seccomp | capabilities(7) | Linux man-pages | <https://man7.org/linux/man-pages/man7/capabilities.7.html> |
| seccomp | Seccomp BPF | kernel.org | <https://docs.kernel.org/userspace-api/seccomp_filter.html> |
| Memory | Compiler Options Hardening Guide | OpenSSF | <https://best.openssf.org/Compiler-Hardening-Guides/Compiler-Options-Hardening-Guide-for-C-and-C++.html> |
| Memory | Debian Hardening | Debian | <https://wiki.debian.org/Hardening> |
| systemd | systemd.exec(5) | freedesktop.org | <https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html> |
| systemd | systemd-analyze(1) | Linux man-pages | <https://man7.org/linux/man-pages/man1/systemd-analyze.1.html> |
| Filesystem | CIS DIL Benchmark | NIST/CIS | <https://ncp.nist.gov/checklist/1129> |
| Filesystem | CIS Benchmarks | CIS | <https://www.cisecurity.org/cis-benchmarks/> |
| Filesystem | OpenSCAP | OpenSCAP | <https://www.open-scap.org/> |
| Audit | auditd(8) | Linux Audit | <https://man7.org/linux/man-pages/man8/auditd.8.html> |
| Audit | SCAP Security Guide | ComplianceAsCode | <https://github.com/ComplianceAsCode/content> |
| Audit | Lynis | CISOfy | <https://cisofy.com/lynis/> |
| Catalog | CWE | MITRE | <https://cwe.mitre.org/> |
| Catalog | ATT&CK | MITRE | <https://attack.mitre.org/> |
| Catalog | KEV | CISA | <https://www.cisa.gov/known-exploited-vulnerabilities-catalog> |
| Catalog | NVD | NIST | <https://nvd.nist.gov/> |
<!-- AGENTTEAMS:END linux_hardening -->

## Operational integration

1. Refresh judgement against these primary sources during security reviews of
   Linux/native targets; the URLs are the current-truth authorities, not this file.
2. Route high-priority platform gaps into `@security` review gates before execution.
3. Tie remediation to owners, controls (CIS/SSG), and verification (auditd/OpenSCAP/Lynis).
4. Escalate unresolved, exploitation-likely gaps to `@orchestrator` with a HALT recommendation.
