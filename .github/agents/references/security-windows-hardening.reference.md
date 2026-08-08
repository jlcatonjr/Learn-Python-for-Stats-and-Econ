# Windows Security Hardening — LearnPythonStatsEcon

<!--
SECTION MANIFEST — security-windows-hardening.reference.template.md
| section_id         | designation   | notes                                                |
|--------------------|---------------|------------------------------------------------------|
| windows_hardening  | FENCED        | Curated Windows hardening baseline + verified sources |
-->

Platform-specific hardening baseline for `@security` when a project **builds,
runs, is distributed for, or is developed on Windows** — native apps, services,
drivers, or code signed for distribution. It is the systems-tier companion to the
low-level / memory-safety screening in `.github/agents/security.agent.md`: that
block screens *code*; this reference screens the *Windows platform* the code runs
on. Parallel in structure to the Linux and macOS hardening references.

This is a **curated baseline of authoritative guidance**, not a live threat feed
(that is `references/security-vulnerability-watch.reference.md`). Every source in
the registry is a primary authority (Microsoft Learn, MSRC, NIST/MITRE, CIS).
Per Rule S-3 (Reference Integrity), do not add a source here without verifying it
resolves to the named authority.

<!-- AGENTTEAMS:BEGIN windows_hardening v=1 -->
## How `@security` uses this reference

- **Scope gate:** consult this reference only for Windows deployment/build/distribution targets. Skip for projects with no Windows surface.
- **Screen, don't remediate:** `@security` is read-only. Flag an unmet control as a finding, route remediation to the owning agent, and escalate exploitation-likely gaps to `@orchestrator` with a HALT recommendation.
- **Tie to the code tier:** platform gaps compound code-level classes (out-of-bounds write CWE-787, use-after-free CWE-416, command injection CWE-78). A memory bug inside a CFG/CET-protected, AppContainer-isolated process on a VBS/HVCI host is far less exploitable than the same bug on an unhardened host.

## 1. System integrity, kernel & secure boot

Establish a measured, integrity-protected boot and kernel. Require **Secure
Boot** and **Measured Boot**; enable **Virtualization-Based Security (VBS)** and
**HVCI / Memory Integrity** so kernel code integrity is enforced in an isolated
VTL; enable **Kernel DMA Protection** against drive-by DMA (Thunderbolt/USB4/PCIe);
require signed kernel-mode drivers.

- Secure the Windows boot process (Secure + Measured Boot, ELAM) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/operating-system-security/system-security/secure-the-windows-10-boot-process>
- Virtualization-based Security (VBS) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-vbs>
- Enable memory integrity (HVCI) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity>
- Kernel DMA Protection — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/hardware-security/kernel-dma-protection-for-thunderbolt>
- Driver signing — Microsoft Learn — <https://learn.microsoft.com/en-us/windows-hardware/drivers/install/driver-signing>

## 2. Privilege-escalation vectors & privilege model

Enforce least privilege on identity and tokens. Keep **UAC** at its default or
stricter (Admin Approval Mode); understand **integrity levels / Mandatory
Integrity Control (MIC)**; enable **LSA Protection (RunAsPPL)** and **Credential
Guard** to protect secrets in LSASS; rotate local-admin passwords with **Windows
LAPS**; follow the **Enterprise access model** (tiering). Landmark elevations:
HiveNightmare/SeriousSAM (CVE-2021-36934), Win32k EoP (CVE-2021-1732), Zerologon
(CVE-2020-1472).

- User Account Control — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/>
- Mandatory Integrity Control (tokens & integrity levels) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control>
- Configure added LSA protection — Microsoft Learn — <https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection>
- Credential Guard overview — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/>
- Windows LAPS overview — Microsoft Learn — <https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview>
- Enterprise access model — Microsoft Learn — <https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model>

## 3. Mandatory access control / application control

Control what executes. Enforce **App Control for Business (WDAC)** as the true
code-integrity boundary; use **AppLocker** as defense-in-depth. **Smart App
Control** is consumer-only: it starts in evaluation mode, cannot be turned on for
an existing install (only via a clean Windows 11 install), and is not
policy-enforceable — rely on WDAC for a managed boundary. Treat "allow
unsigned/anything" policies as findings.

- App Control for Business (WDAC) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/appcontrol>
- AppLocker overview — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview>
- Smart App Control FAQ — Microsoft Support — <https://support.microsoft.com/en-us/windows/smart-app-control-frequently-asked-questions-285ea03d-fa88-4d56-882e-6698afdb7003>

## 4. Application isolation, sandboxing & containers

Isolate untrusted and network-facing code. Run components in an **AppContainer**;
test/execute untrusted software in **Windows Sandbox**; adopt **Win32 app
isolation** for packaged desktop apps; use **Hyper-V isolation** for
strong-boundary Windows containers rather than process isolation for untrusted
workloads.

- AppContainer isolation — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation>
- Windows Sandbox — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/>
- Win32 app isolation overview — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/secauthz/app-isolation-overview>
- Isolation modes (process vs. Hyper-V) — Microsoft Learn — <https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container>

## 5. Capability & process-mitigation restriction

Shrink each process's attack surface. Apply **Exploit Protection** / per-process
mitigation policies (`SetProcessMitigationPolicy`), including syscall-disable and
child-process restrictions; declare least-privilege **AppContainer** capabilities;
enable child-process blocking (`ChildProcess` / DisallowChildProcessCreation) and
`BlockDynamicCode` where compatible.

- Apply mitigations (Exploit Protection) — Microsoft Learn — <https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection>
- SetProcessMitigationPolicy — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessmitigationpolicy>
- AppContainer for legacy apps (capability model) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-for-legacy-applications->

## 6. Userspace memory-protection & exploit mitigations

Compile and configure so the memory-safety defects in the low-level code block
are harder to weaponize: **DEP**, **ASLR/ForceASLR**, **Control Flow Guard
(CFG)**, hardware-enforced **CET / shadow stack**, and **Arbitrary Code Guard
(ACG)**. Enforce per-app via Exploit Protection; treat a shipped binary missing
`/guard:cf`, `/DYNAMICBASE`, `/NXCOMPAT`, `/CETCOMPAT` as a finding.

- Exploit protection reference (DEP/ASLR/CFG/CET/ACG) — Microsoft Learn — <https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection-reference>
- Data Execution Prevention — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/memory/data-execution-prevention>
- Control Flow Guard — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/secbp/control-flow-guard>

## 7. Service / daemon hardening

Run services least-privilege. Use **group Managed Service Accounts (gMSA)** with
auto-rotated passwords instead of shared/interactive service accounts; enable
**Attack Surface Reduction (ASR)** rules; scope per-service ACLs and rights.

- Group Managed Service Accounts overview — Microsoft Learn — <https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview>
- Attack surface reduction (ASR) rules overview — Microsoft Learn — <https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-overview>
- Service security and access rights — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights>

## 8. Filesystem, disk encryption & secrets at rest

Encrypt and protect data. Require **BitLocker** full-volume encryption (TPM-bound);
use **EFS** for per-file needs; store secrets via **DPAPI/CNG** rather than
plaintext; prefer passwordless **Windows Hello for Business**; set least-privilege
**NTFS ACLs**.

- BitLocker overview — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/>
- File Encryption (EFS) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/fileio/file-encryption>
- CNG DPAPI (secrets at rest) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/seccng/cng-dpapi>
- Windows Hello for Business — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/>
- File security and access rights (NTFS ACLs) — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights>

## 9. Auditing, detection & compliance

Baseline and monitor. Apply **Microsoft Security Baselines** via the **Security
Compliance Toolkit (SCT)** and/or a **CIS Microsoft Windows Benchmark**; collect
**Windows Event Log** + **Sysmon**; run **Microsoft Defender for Endpoint**;
track configuration drift.

- Security baselines guide — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines>
- Microsoft Security Compliance Toolkit — Microsoft Learn — <https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10>
- CIS Microsoft Windows Desktop Benchmarks — Center for Internet Security — <https://www.cisecurity.org/benchmark/microsoft_windows_desktop>
- Sysmon (Sysinternals) — Microsoft — <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon>
- Microsoft Defender for Endpoint — Microsoft Learn — <https://learn.microsoft.com/en-us/defender-endpoint/>

## 10. Vulnerability & exploit-class catalogs (cross-cutting)

Anchor findings to authoritative catalogs.

- Microsoft Security Response Center (MSRC) — Microsoft — <https://www.microsoft.com/en-us/msrc>
- Security Update Guide (searchable CVEs) — MSRC — <https://msrc.microsoft.com/update-guide>
- MITRE ATT&CK (Enterprise / Windows matrix) — MITRE — <https://attack.mitre.org/matrices/enterprise/windows/>
- Common Weakness Enumeration (CWE) — MITRE — <https://cwe.mitre.org/>
- National Vulnerability Database (CVE / CVSS) — NIST — <https://nvd.nist.gov/>
- Known Exploited Vulnerabilities (KEV) Catalog — CISA — <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>

## Landmark Windows privilege-escalation / notable exploits (illustrative)

Concrete classes to recognize; each links to its NVD entry.

- **PrintNightmare** (CVE-2021-34527) — Print Spooler improper privileged file ops → RCE/LPE — <https://nvd.nist.gov/vuln/detail/CVE-2021-34527>
- **Win32k EoP** (CVE-2021-1732) — Win32k out-of-bounds write elevation of privilege — <https://nvd.nist.gov/vuln/detail/CVE-2021-1732>
- **HiveNightmare / SeriousSAM** (CVE-2021-36934) — overly permissive ACLs on SAM/registry hives → LPE — <https://nvd.nist.gov/vuln/detail/CVE-2021-36934>
- **Zerologon** (CVE-2020-1472) — Netlogon (MS-NRPC) crypto flaw → domain-controller takeover — <https://nvd.nist.gov/vuln/detail/CVE-2020-1472>
- **Win32k EoP** (CVE-2022-21882) — Win32k OOB-write elevation (bypass of CVE-2021-1732) — <https://nvd.nist.gov/vuln/detail/CVE-2022-21882>

## Source registry (authoritative, verified)

Some Microsoft slugs redirect to renamed canonical pages (HVCI → "Enable memory
integrity"; WDAC → "App Control for Business"; Hyper-V → "Isolation modes"); the
canonical URLs are used here. MSRC Security Update Guide and CISA KEV are
client-side apps / bot-blocked; their URLs are canonical and load in a browser.

| Domain | Source | Publisher | URL |
|---|---|---|---|
| Boot | Secure + Measured Boot | Microsoft | <https://learn.microsoft.com/en-us/windows/security/operating-system-security/system-security/secure-the-windows-10-boot-process> |
| Boot | VBS | Microsoft | <https://learn.microsoft.com/en-us/windows-hardware/design/device-experiences/oem-vbs> |
| Boot | HVCI / Memory Integrity | Microsoft | <https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity> |
| Boot | Kernel DMA Protection | Microsoft | <https://learn.microsoft.com/en-us/windows/security/hardware-security/kernel-dma-protection-for-thunderbolt> |
| Boot | Driver signing | Microsoft | <https://learn.microsoft.com/en-us/windows-hardware/drivers/install/driver-signing> |
| Priv-esc | User Account Control | Microsoft | <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/user-account-control/> |
| Priv-esc | Mandatory Integrity Control | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/secauthz/mandatory-integrity-control> |
| Priv-esc | LSA Protection | Microsoft | <https://learn.microsoft.com/en-us/windows-server/security/credentials-protection-and-management/configuring-additional-lsa-protection> |
| Priv-esc | Credential Guard | Microsoft | <https://learn.microsoft.com/en-us/windows/security/identity-protection/credential-guard/> |
| Priv-esc | Windows LAPS | Microsoft | <https://learn.microsoft.com/en-us/windows-server/identity/laps/laps-overview> |
| Priv-esc | Enterprise access model | Microsoft | <https://learn.microsoft.com/en-us/security/privileged-access-workstations/privileged-access-access-model> |
| App-control | App Control for Business (WDAC) | Microsoft | <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/appcontrol> |
| App-control | AppLocker | Microsoft | <https://learn.microsoft.com/en-us/windows/security/application-security/application-control/app-control-for-business/applocker/applocker-overview> |
| App-control | Smart App Control | Microsoft | <https://support.microsoft.com/en-us/windows/smart-app-control-frequently-asked-questions-285ea03d-fa88-4d56-882e-6698afdb7003> |
| Isolation | AppContainer isolation | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation> |
| Isolation | Windows Sandbox | Microsoft | <https://learn.microsoft.com/en-us/windows/security/application-security/application-isolation/windows-sandbox/> |
| Isolation | Win32 app isolation | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/secauthz/app-isolation-overview> |
| Isolation | Isolation modes (Hyper-V) | Microsoft | <https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/hyperv-container> |
| Mitigation | Exploit Protection | Microsoft | <https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection> |
| Mitigation | SetProcessMitigationPolicy | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-setprocessmitigationpolicy> |
| Memory | Exploit protection reference | Microsoft | <https://learn.microsoft.com/en-us/defender-endpoint/exploit-protection-reference> |
| Memory | Data Execution Prevention | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/memory/data-execution-prevention> |
| Memory | Control Flow Guard | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/secbp/control-flow-guard> |
| Service | Group Managed Service Accounts | Microsoft | <https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-managed-service-accounts/group-managed-service-accounts/group-managed-service-accounts-overview> |
| Service | ASR rules overview | Microsoft | <https://learn.microsoft.com/en-us/defender-endpoint/attack-surface-reduction-rules-overview> |
| Service | Service security & access rights | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/services/service-security-and-access-rights> |
| Filesystem | BitLocker | Microsoft | <https://learn.microsoft.com/en-us/windows/security/operating-system-security/data-protection/bitlocker/> |
| Filesystem | EFS (file encryption) | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/fileio/file-encryption> |
| Filesystem | CNG DPAPI | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/seccng/cng-dpapi> |
| Filesystem | Windows Hello for Business | Microsoft | <https://learn.microsoft.com/en-us/windows/security/identity-protection/hello-for-business/> |
| Filesystem | File security & access rights | Microsoft | <https://learn.microsoft.com/en-us/windows/win32/fileio/file-security-and-access-rights> |
| Audit | Security baselines guide | Microsoft | <https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/windows-security-baselines> |
| Audit | Security Compliance Toolkit | Microsoft | <https://learn.microsoft.com/en-us/windows/security/operating-system-security/device-management/windows-security-configuration-framework/security-compliance-toolkit-10> |
| Audit | CIS Microsoft Windows Benchmarks | CIS | <https://www.cisecurity.org/benchmark/microsoft_windows_desktop> |
| Audit | Sysmon | Microsoft | <https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon> |
| Audit | Microsoft Defender for Endpoint | Microsoft | <https://learn.microsoft.com/en-us/defender-endpoint/> |
| Catalog | MSRC | Microsoft | <https://www.microsoft.com/en-us/msrc> |
| Catalog | Security Update Guide | Microsoft | <https://msrc.microsoft.com/update-guide> |
| Catalog | ATT&CK Windows matrix | MITRE | <https://attack.mitre.org/matrices/enterprise/windows/> |
| Catalog | CWE | MITRE | <https://cwe.mitre.org/> |
| Catalog | NVD | NIST | <https://nvd.nist.gov/> |
| Catalog | KEV | CISA | <https://www.cisa.gov/known-exploited-vulnerabilities-catalog> |
<!-- AGENTTEAMS:END windows_hardening -->

<!-- AGENTTEAMS:BEGIN operational_integration v=1 -->
## Operational integration

1. Refresh judgement against these primary sources during security reviews of Windows targets; the URLs are the current-truth authorities, not this file.
2. Route high-priority platform gaps into `@security` review gates before execution.
3. Tie remediation to owners, controls (Security Baselines / CIS), and verification (Event Log / Sysmon / Defender).
4. Escalate unresolved, exploitation-likely gaps to `@orchestrator` with a HALT recommendation.
<!-- AGENTTEAMS:END operational_integration -->

## Operational integration

1. Refresh judgement against these primary sources during security reviews of Windows targets; the URLs are the current-truth authorities, not this file.
2. Route high-priority platform gaps into `@security` review gates before execution.
3. Tie remediation to owners, controls (Security Baselines / CIS), and verification (Event Log / Sysmon / Defender).
4. Escalate unresolved, exploitation-likely gaps to `@orchestrator` with a HALT recommendation.
