# macOS Security Hardening — LearnPythonStatsEcon

<!--
SECTION MANIFEST — security-macos-hardening.reference.template.md
| section_id       | designation   | notes                                              |
|------------------|---------------|----------------------------------------------------|
| macos_hardening  | FENCED        | Curated macOS hardening baseline + verified sources |
-->

Platform-specific hardening baseline for `@security` when a project **builds,
runs, is distributed for, or is developed on macOS** — native apps, CLI tools,
launchd services, or code signed/notarized for distribution. It is the
systems-tier companion to the low-level / memory-safety screening in
`.github/agents/security.agent.md`: that block screens *code*; this reference
screens the *macOS platform* the code runs on. Parallel in structure to the
Linux and Windows hardening references.

This is a **curated baseline of authoritative guidance**, not a live threat feed
(that is `references/security-vulnerability-watch.reference.md`). Every source in
the registry is a primary authority (Apple Platform Security, Apple Developer,
NIST, CIS, MITRE). Per Rule S-3 (Reference Integrity), do not add a source here
without verifying it resolves to the named authority.

<!-- AGENTTEAMS:BEGIN macos_hardening v=1 -->
## How `@security` uses this reference

- **Scope gate:** consult this reference only for macOS deployment/build/distribution targets. Skip for projects with no macOS surface.
- **Screen, don't remediate:** `@security` is read-only. Flag an unmet control as a finding, route remediation to the owning agent, and escalate exploitation-likely gaps to `@orchestrator` with a HALT recommendation.
- **Tie to the code tier:** platform gaps compound code-level classes (out-of-bounds write CWE-787, use-after-free CWE-416, command injection CWE-78). A memory bug inside an App-Sandboxed, hardened-runtime, PAC-protected process is far less exploitable than the same bug in an unsandboxed one.

## 1. System integrity, kernel & secure boot

Keep the platform's own integrity guarantees intact. Never disable **System
Integrity Protection (SIP)** in production or in shipped guidance; keep the
**Signed System Volume (SSV)** seal intact; on Apple silicon keep **Full
Security** boot (avoid Reduced/Permissive); keep **Gatekeeper** enabled so only
signed + notarized code runs. Prefer **System Extensions / DriverKit** over
legacy kernel extensions (kexts), which weaken kernel integrity.

- System Integrity Protection — Apple Platform Security — <https://support.apple.com/guide/security/system-integrity-protection-secb7ea06b49/web>
- Signed System Volume security — Apple Platform Security — <https://support.apple.com/guide/security/signed-system-volume-security-secd698747c9/web>
- Boot process for a Mac with Apple silicon — Apple Platform Security — <https://support.apple.com/guide/security/boot-process-secac71d5623/web>
- Gatekeeper and runtime protection — Apple Platform Security — <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web>
- System Extensions / DriverKit — Apple Developer — <https://developer.apple.com/system-extensions/>

## 2. Privilege-escalation vectors & privilege model

Run as a **standard** (non-admin) account for daily use; reserve admin for
explicit tasks. Keep `sudo` least-privilege and patched. Respect **TCC**
(Transparency, Consent & Control): never instruct users to blanket-approve Full
Disk Access or bypass consent prompts; request only the entitlements/privacy
scopes actually needed. Use **Authorization Services** for privileged operations
rather than running whole tools as root. Landmark privilege/consent bypass:
powerdir TCC bypass (CVE-2021-30970). (Shrootless, CVE-2021-30892, is a related
SIP-integrity bypass — see §1.)

- Protecting app access to user data (TCC model) — Apple Platform Security — <https://support.apple.com/guide/security/protecting-app-access-to-user-data-secc01781f46/web>
- Authorization Services — Apple Developer — <https://developer.apple.com/documentation/security/authorization-services>
- Change Users & Groups settings on Mac (account model) — Apple Support — <https://support.apple.com/guide/mac-help/change-users-groups-settings-mtusr001/mac>

## 3. Mandatory access control / application control

Confine and sign code. Adopt the **App Sandbox** for distributed apps; **code
sign** and **notarize** everything shipped; enable the **Hardened Runtime**;
grant **entitlements** narrowly and treat broad exceptions (e.g. disabling
library validation, allowing unsigned executable memory) as findings.

- App Sandbox — Apple Developer — <https://developer.apple.com/documentation/security/app-sandbox>
- Code Signing Services — Apple Developer — <https://developer.apple.com/documentation/security/code-signing-services>
- Notarizing macOS software before distribution — Apple Developer — <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution>
- Hardened Runtime — Apple Developer — <https://developer.apple.com/documentation/security/hardened-runtime>
- Entitlements (key reference) — Apple Developer — <https://developer.apple.com/documentation/bundleresources/entitlements>

## 4. Application isolation, sandboxing & containers

Isolate components and mediate IPC. Pair the App Sandbox with **XPC** for
privilege-separated helpers; use the **Endpoint Security** framework for
monitoring rather than kernel hooks. Sandbox untrusted execution via the App
Sandbox; the legacy `sandbox-exec`/Seatbelt profile mechanism is deprecated and
has no supported public API — do not build new isolation on it.

- App Sandbox — Apple Developer — <https://developer.apple.com/documentation/security/app-sandbox>
- XPC — Apple Developer — <https://developer.apple.com/documentation/xpc>
- Endpoint Security — Apple Developer — <https://developer.apple.com/documentation/endpointsecurity>

## 5. Capability & process-mitigation restriction

Minimize what a signed process may do. Enable the **Hardened Runtime** and grant
its capability exceptions (JIT, unsigned memory, `DYLD_*` env vars, debugging)
only when strictly required; keep **library validation** on so only
same-team/Apple-signed libraries load.

- Hardened Runtime (capabilities & exceptions) — Apple Developer — <https://developer.apple.com/documentation/security/hardened-runtime>
- Disable Library Validation entitlement (the opt-out to avoid) — Apple Developer — <https://developer.apple.com/documentation/bundleresources/entitlements/com_apple_security_cs_disable-library-validation>

## 6. Userspace memory-protection & exploit mitigations

Lean on Apple-silicon and OS mitigations that blunt the memory-safety defects
screened in the low-level code block: **Pointer Authentication (PAC)** on Apple
silicon, Kernel Integrity Protection, ASLR, and Execute-Never (NX). PAC is a
platform property user-mode apps receive automatically — arm64e is a system/kernel
ABI, **not** a supported third-party distribution target, so do not ship arm64e.
Keep the Hardened Runtime and library validation on.

- Operating system integrity (PAC, KIP, page protection) — Apple Platform Security — <https://support.apple.com/guide/security/operating-system-integrity-sec8b776536b/web>
- Preparing your app to work with pointer authentication — Apple Developer — <https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication>

## 7. Service / daemon hardening

Run background work as least-privilege launchd jobs. Prefer **LaunchAgents**
(per-user) over root **LaunchDaemons** where possible; scope daemon privileges;
expose functionality through **XPC services** rather than a privileged always-on
listener. Sign and notarize daemons like any other code.

- Creating Launch Daemons and Agents — Apple Developer (Archive) — <https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html>
- XPC (privilege-separated services) — Apple Developer — <https://developer.apple.com/documentation/xpc>

## 8. Filesystem, disk encryption & secrets at rest

Encrypt and protect data. Require **FileVault** on portable/endpoint Macs; store
secrets in the **Keychain** (not plists, env, or app bundles); apply **Data
Protection** classes; respect file **quarantine** (`com.apple.quarantine`) rather
than stripping it. Keep credentials out of world-readable locations.

- Volume encryption with FileVault — Apple Platform Security — <https://support.apple.com/guide/security/volume-encryption-with-filevault-sec4c6dc1b6e/web>
- Keychain services — Apple Developer — <https://developer.apple.com/documentation/security/keychain-services>
- Data Protection overview — Apple Platform Security — <https://support.apple.com/guide/security/data-protection-overview-secf6276da8a/web>

## 9. Auditing, detection & compliance

Make hardening measurable. Baseline against the **macOS Security Compliance
Project (mSCP)** / **NIST SP 800-219** and the **CIS Apple macOS Benchmark**;
collect **Unified Logging** and **Endpoint Security** events; track drift over time.

- macOS Security Compliance Project (mSCP) — NIST (usnistgov) — <https://github.com/usnistgov/macos_security>
- NIST SP 800-219 Rev. 1 (automated macOS config guidance) — NIST CSRC — <https://csrc.nist.gov/pubs/sp/800/219/r1/final>
- CIS Apple macOS Benchmarks — Center for Internet Security — <https://www.cisecurity.org/benchmark/apple_os>
- Unified Logging (`os_log`) — Apple Developer — <https://developer.apple.com/documentation/os/logging>

## 10. Vulnerability & exploit-class catalogs (cross-cutting)

Anchor findings to authoritative catalogs.

- Apple Platform Security (guide + PDF) — Apple — <https://support.apple.com/guide/security/welcome/web>
- Apple security releases (advisory index) — Apple — <https://support.apple.com/en-us/HT201222>
- MITRE ATT&CK (Enterprise / macOS matrix) — MITRE — <https://attack.mitre.org/matrices/enterprise/macos/>
- Common Weakness Enumeration (CWE) — MITRE — <https://cwe.mitre.org/>
- National Vulnerability Database (CVE / CVSS) — NIST — <https://nvd.nist.gov/>
- Known Exploited Vulnerabilities (KEV) Catalog — CISA — <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>

## Landmark macOS privilege / integrity-bypass exploits (illustrative)

Concrete classes to recognize; each links to its NVD entry.

- **Shrootless** (CVE-2021-30892) — SIP bypass via an inherited-permissions issue → modify protected filesystem — <https://nvd.nist.gov/vuln/detail/CVE-2021-30892>
- **Gatekeeper bypass** (CVE-2021-30657) — malicious app bypasses Gatekeeper checks (exploited by Shlayer) — <https://nvd.nist.gov/vuln/detail/CVE-2021-30657>
- **powerdir** (CVE-2021-30970) — TCC/privacy bypass; app reaches protected user data — <https://nvd.nist.gov/vuln/detail/CVE-2021-30970>
- **Achilles** (CVE-2022-42821) — Gatekeeper bypass via crafted extended attributes — <https://nvd.nist.gov/vuln/detail/CVE-2022-42821>
- **Migraine** (CVE-2023-32369) — SIP bypass; app modifies protected filesystem regions — <https://nvd.nist.gov/vuln/detail/CVE-2023-32369>

## Source registry (authoritative, verified)

Apple developer.apple.com pages are JavaScript apps (title + HTTP 200 confirmed;
body not machine-fetchable). The `launchd` job guidance is cited via Apple's
Documentation Archive (an Apple-hosted page). Every source below resolves to a
primary authority.

| Domain | Source | Publisher | URL |
|---|---|---|---|
| Integrity | System Integrity Protection | Apple | <https://support.apple.com/guide/security/system-integrity-protection-secb7ea06b49/web> |
| Integrity | Signed System Volume | Apple | <https://support.apple.com/guide/security/signed-system-volume-security-secd698747c9/web> |
| Integrity | Apple-silicon boot process | Apple | <https://support.apple.com/guide/security/boot-process-secac71d5623/web> |
| Integrity | Gatekeeper & runtime protection | Apple | <https://support.apple.com/guide/security/gatekeeper-and-runtime-protection-sec5599b66df/web> |
| Integrity | System Extensions | Apple | <https://developer.apple.com/system-extensions/> |
| Priv-esc | TCC / app access to user data | Apple | <https://support.apple.com/guide/security/protecting-app-access-to-user-data-secc01781f46/web> |
| Priv-esc | Authorization Services | Apple | <https://developer.apple.com/documentation/security/authorization-services> |
| Priv-esc | Account model | Apple | <https://support.apple.com/guide/mac-help/change-users-groups-settings-mtusr001/mac> |
| App-control | App Sandbox | Apple | <https://developer.apple.com/documentation/security/app-sandbox> |
| App-control | Code Signing Services | Apple | <https://developer.apple.com/documentation/security/code-signing-services> |
| App-control | Notarization | Apple | <https://developer.apple.com/documentation/security/notarizing-macos-software-before-distribution> |
| App-control | Hardened Runtime | Apple | <https://developer.apple.com/documentation/security/hardened-runtime> |
| App-control | Entitlements | Apple | <https://developer.apple.com/documentation/bundleresources/entitlements> |
| Isolation | XPC | Apple | <https://developer.apple.com/documentation/xpc> |
| Isolation | Endpoint Security | Apple | <https://developer.apple.com/documentation/endpointsecurity> |
| Isolation | App Sandbox | Apple | <https://developer.apple.com/documentation/security/app-sandbox> |
| Memory | Operating system integrity (PAC) | Apple | <https://support.apple.com/guide/security/operating-system-integrity-sec8b776536b/web> |
| Memory | Pointer authentication (app adoption) | Apple | <https://developer.apple.com/documentation/security/preparing-your-app-to-work-with-pointer-authentication> |
| Service | Launch Daemons and Agents | Apple | <https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/CreatingLaunchdJobs.html> |
| Filesystem | FileVault volume encryption | Apple | <https://support.apple.com/guide/security/volume-encryption-with-filevault-sec4c6dc1b6e/web> |
| Filesystem | Keychain services | Apple | <https://developer.apple.com/documentation/security/keychain-services> |
| Filesystem | Data Protection overview | Apple | <https://support.apple.com/guide/security/data-protection-overview-secf6276da8a/web> |
| Audit | macOS Security Compliance Project | NIST | <https://github.com/usnistgov/macos_security> |
| Audit | NIST SP 800-219 Rev. 1 | NIST | <https://csrc.nist.gov/pubs/sp/800/219/r1/final> |
| Audit | CIS Apple macOS Benchmarks | CIS | <https://www.cisecurity.org/benchmark/apple_os> |
| Audit | Unified Logging | Apple | <https://developer.apple.com/documentation/os/logging> |
| Catalog | Apple Platform Security | Apple | <https://support.apple.com/guide/security/welcome/web> |
| Catalog | Apple security releases | Apple | <https://support.apple.com/en-us/HT201222> |
| Catalog | ATT&CK macOS matrix | MITRE | <https://attack.mitre.org/matrices/enterprise/macos/> |
| Catalog | CWE | MITRE | <https://cwe.mitre.org/> |
| Catalog | NVD | NIST | <https://nvd.nist.gov/> |
| Catalog | KEV | CISA | <https://www.cisa.gov/known-exploited-vulnerabilities-catalog> |
<!-- AGENTTEAMS:END macos_hardening -->

<!-- AGENTTEAMS:BEGIN operational_integration v=1 -->
## Operational integration

1. Refresh judgement against these primary sources during security reviews of macOS targets; the URLs are the current-truth authorities, not this file.
2. Route high-priority platform gaps into `@security` review gates before execution.
3. Tie remediation to owners, controls (mSCP/CIS), and verification (Unified Logging / Endpoint Security).
4. Escalate unresolved, exploitation-likely gaps to `@orchestrator` with a HALT recommendation.
<!-- AGENTTEAMS:END operational_integration -->

## Operational integration

1. Refresh judgement against these primary sources during security reviews of macOS targets; the URLs are the current-truth authorities, not this file.
2. Route high-priority platform gaps into `@security` review gates before execution.
3. Tie remediation to owners, controls (mSCP/CIS), and verification (Unified Logging / Endpoint Security).
4. Escalate unresolved, exploitation-likely gaps to `@orchestrator` with a HALT recommendation.
