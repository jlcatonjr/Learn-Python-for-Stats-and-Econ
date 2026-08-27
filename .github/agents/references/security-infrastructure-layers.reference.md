# Infrastructure Security Layers — LearnPythonStatsEcon

<!--
SECTION MANIFEST — security-infrastructure-layers.reference.template.md
| section_id                    | designation   | notes                                                     |
|-------------------------------|---------------|-----------------------------------------------------------|
| infra_security_model          | FENCED        | Scope gate, agentic-vs-infrastructure distinction, the 8-layer model, honest ceiling, who builds vs who reviews |
| infra_security_layers         | FENCED        | L0–L7: development, selection criteria, anchor tools, control verb, maintenance loop |
| infra_security_tool_catalog   | FENCED        | Consolidated verified open-source tool table (single license home) + currency stamp |
| operational_integration       | FENCED        | How this reference is consumed and kept current           |
| project_infra_security_notes  | USER-EDITABLE | Project records its own layer choices, tools, and deviations |
-->

Curated, source-grounded model for the **security of the infrastructure this project builds and
operates** — the deployed program, server, or service — organized as eight defense-in-depth layers,
each with the open-source applications that implement it. It is the *deployed-system* companion to
the agentic-security surface in `security.agent.md` and the per-OS baselines in
`security-{linux,macos,windows}-hardening.reference.md`.

This is a **curated baseline that points to authoritative guidance and open-source tools**, not a
live feed and not a guarantee. Every layer is grounded in primary standards (NIST, IETF RFCs,
OWASP, CIS, MITRE); every tool was verified against its official repository. The
Reference-Integrity rule below governs additions to this file.

<!-- AGENTTEAMS:BEGIN infra_security_model v=1 -->
## 0. Scope, distinction, and honest ceiling (read first)

- **Scope gate.** This reference applies only to projects that **build, deploy, run, or operate a
  program, server, or service**. If LearnPythonStatsEcon ships no deployed software (e.g. a pure
  research, writing, or documentation project), skip it — as with the per-OS hardening references.
- **Infrastructure security ≠ agent security.** The `@security` sentinel governs the *agentic /
  build process*: destructive-operation clearance, credential leakage into deliverables,
  prompt-injection / OWASP LLM Top 10 screening, install vetting. **This reference governs the
  *deployed system*** the project produces: its identity, cryptography, network, application,
  detection, and resilience posture. The two are adjacent and must not be collapsed — hardening the
  agent team does not harden the production server, and vice versa.
- **Who builds vs who reviews.** The controls below are **built by the producing / workstream
  agents** that own the deployed system, and **verified by `@technical-validator`**. `@security`
  **reviews against** this reference (a checklist for a service-deploying project); it does not
  build these controls (it is read-only).
- **Honest ceiling (binding).** A reference *informs*; it secures nothing by itself. A control
  provides security only once **deployed and tested** on the real target. State posture as
  "engages as tested on this target," never "verified" or "secure." Positive tests show a boundary
  engages; they do not prove it cannot be bypassed (base-rate and sandbox-completeness limits).
- **Reference integrity (binding).** New sources and tools enter this file only after verifying
  that each resolves to the named authority (the security Reference-Integrity rule); an unverified
  addition is a finding, not an entry.

## 1. The layered model

Security infrastructure is a **layered** program cross-cut by a **lifecycle**. The layers degrade
independently — a strong one does not compensate for an absent one — so assess each separately
rather than as one score (the reason CIS uses implementation groups and NIST uses control
baselines). Weight the layers to the system's **actual attack surface**: a public server is heavy
at L1/L2/L5; an internal batch host is heavier at L3/L6/L7. Every control at every layer moves
through the same lifecycle: **design → build → baseline → tune → operate → respond → review** —
and infrastructure most often decays at *baseline, tune,* and *review*, not at build. Two
disciplines are therefore structural, not optional: **baseline before you alert**, and **an
untested backup is a hypothesis, not a control.**

| Layer | Concern | Grounding |
|---|---|---|
| L0 | Governance, risk & compliance | NIST CSF 2.0; SP 800-53; SP 800-37; CIS Controls v8.1 |
| L1 | Identity, authentication, authorization | OAuth 2.1 / OIDC; SP 800-63B; RBAC; ABAC (SP 800-162) |
| L2 | Cryptography, secrets & key management | TLS 1.3 (RFC 8446); SP 800-52r2; SP 800-57; ACME (RFC 8555) |
| L3 | Host & workload hardening | SP 800-123; SP 800-190; CIS Benchmarks; the per-OS hardening refs |
| L4 | Network & perimeter | SP 800-41r1; SP 800-94; zero trust (SP 800-207) |
| L5 | Application & software supply chain | OWASP Top 10 / ASVS; SSDF (SP 800-218); SLSA; SBOM |
| L6 | Detection, logging & SIEM | SP 800-92; SP 800-137; MITRE ATT&CK; base-rate discipline |
| L7 | Resilience, backup & incident response | SP 800-34; SP 800-61; RFC 3227; 3-2-1 backups |

Full source grounding: the backing research at
`agentteams-research/security-infrastructure/` (where present) and the standards named above.
<!-- AGENTTEAMS:END infra_security_model -->

<!-- AGENTTEAMS:BEGIN infra_security_layers v=1 -->
## 2. The eight layers

Each layer states the **development** (what the deployed system should do), **selection criteria**
(how to choose a tool without this list going stale), **anchor tools** (verb in parentheses; full
licenses in §3), and the **maintenance loop**. Tools are open-source unless a §3 flag says
otherwise.

### L0 — Governance, risk & compliance
- **Development:** adopt a right-sized control baseline (a CIS Implementation Group 1 floor, a CSF
  2.0 profile, or a scaled SP 800-53 baseline) and run a scheduled compliance scan with a
  deviation register. Small systems adopt a defensible subset, not the full catalog.
- **Selection criteria:** prefer a scanner that emits diffs between runs (not a bare score), maps
  to a named benchmark, and runs unattended.
- **Anchor tools:** OpenSCAP + SCAP Security Guide / ComplianceAsCode (compliance-scan), Lynis
  (audit), OPA + Conftest (inline-prevent — policy-as-code gates); cloud posture: Prowler,
  ScoutSuite, Cloud Custodian, Steampipe. CIS Benchmarks are free reference PDFs, not software.
- **Maintenance:** scheduled scan; deviation register; re-baseline on drift.

### L1 — Identity, authentication, authorization
- **Development:** an identity provider and authN model (OIDC), phishing-resistant MFA at the
  assurance level the data warrants, RBAC/ABAC authorization, and forward-auth in front of internal
  services (a policy-enforcement point — an inline reference monitor for requests).
- **Selection criteria:** OIDC-certified; supports the MFA strength you need (WebAuthn/passkeys for
  phishing resistance); authorization decisions externalized from application code.
- **Anchor tools:** Keycloak / Authentik / Zitadel / Ory (Hydra + Kratos) / Dex
  (identity-provision, inline-prevent at the gate); Authelia / oauth2-proxy / Vouch Proxy
  (forward-auth, inline-prevent); OpenFGA / Casbin (authorization engine, inline-prevent).
- **Maintenance:** credential and session rotation; periodic access review; deprovisioning.

### L2 — Cryptography, secrets & key management
- **Development:** TLS 1.3 configured per SP 800-52r2, automated certificate lifecycle (ACME),
  secrets vaulting with rotation, encryption at rest, and artifact signing. **The
  secrets-management gap:** there is no vendor-neutral primary standard for secrets management, so
  this layer names an explicit OSS anchor rather than leaving it implicit (see §3).
- **Selection criteria:** automate certificate renewal (no annual outage); keep the signing/root
  key the only real secret; never hand-roll crypto.
- **Anchor tools:** step-ca / cert-manager / Certbot (PKI + ACME, harden); **OpenBao** (secrets
  store, harden) — the OSS anchor; SOPS + age (encrypted-file-at-rest, harden); Sigstore cosign
  (artifact signing/verify, inline-prevent at deploy); gitleaks / trufflehog (secret scanning,
  detect). Note: HashiCorp Vault is source-available (BUSL), **not open source** — prefer OpenBao.
- **Maintenance:** certificate renewal automation; key rotation and cryptoperiods per SP 800-57.

### L3 — Host & workload hardening
- **Development:** harden the OS and workload. For host-OS hardening, use the authoritative
  per-OS references (do not duplicate them here): `security-linux-hardening.reference.md`,
  `security-macos-hardening.reference.md`, `security-windows-hardening.reference.md`. This layer
  adds **container/workload** hardening, mandatory access control / sandboxing, and host runtime
  detection.
- **Selection criteria:** prefer kernel-enforced boundaries over cooperative checks; measure
  container images against the CIS benchmark for the runtime.
- **Anchor tools:** osquery (detect — host telemetry); AppArmor / SELinux / firejail / bubblewrap
  (inline-prevent — MAC/sandbox); Santa (inline-prevent — macOS binary authorization); Trivy /
  Docker Bench / kube-bench (compliance-scan — container/K8s CIS); Falco (detect — runtime).
- **Maintenance:** re-baseline; CIS deviation register (shared with the per-OS references).

### L4 — Network & perimeter
- **Development:** network segmentation, a host/edge firewall, IDS/NSM, DNS filtering, reactive IP
  blocking, encrypted admin access (VPN), and zero-trust service-to-service (mTLS, links L2).
- **Control-verb precision (do not blur):** *detection* observes and reports; *reactive blocking*
  acts after an observation (e.g. adds an IP to a firewall table); *inline prevention* refuses the
  action in-path. The same engine can be detect or prevent by deployment — Suricata/Snort are IDS
  (detect) or inline IPS (prevent). Platform limits are real (e.g. macOS `pf` cannot run an inline
  IPS; state such limits where prevention is discussed).
- **Anchor tools:** nftables / pf / OPNsense / pfSense CE (inline-prevent — firewall); Suricata /
  Zeek / Snort (detect as IDS/NSM, inline-prevent as IPS); CrowdSec / Fail2ban (reactive-block);
  Pi-hole / AdGuard Home (DNS filtering, inline-prevent) + Unbound (DNSSEC, harden); WireGuard
  (harden — encrypted admin tunnel).
- **Maintenance:** rule tuning against measured false positives (baseline before alert); ruleset
  currency.

### L5 — Application & software supply chain
- **Development:** SAST/DAST in CI, software-composition analysis + SBOM, secret scanning,
  dependency/vulnerability gates, build provenance/signing (SLSA), and OWASP ASVS as acceptance
  criteria. This extends the live package watch in `security-vulnerability-watch.reference.md`
  (the authoritative home for current CVE/OSV data — do not duplicate its feed here).
- **Selection criteria:** gate the build, don't just report; keep scanners and their vuln databases
  current; produce a machine-readable SBOM.
- **Anchor tools:** Semgrep / Bandit (SAST, detect) + OWASP ZAP (DAST, detect); Trivy / Grype +
  Syft / OSV-Scanner / Dependency-Track / OWASP Dependency-Check (SCA + SBOM, detect); gitleaks /
  trufflehog (secret scan, detect); Sigstore cosign / in-toto / slsa-github-generator (provenance,
  inline-prevent at deploy); OpenSSF Scorecard (repo posture, detect). CI gates that fail the
  build are the inline-prevent control.
- **Maintenance:** scanner and advisory-DB currency; triage with a named owner.

### L6 — Detection, logging & SIEM
- **Development:** centralized logging with retention, a SIEM/XDR, runtime detection, detection
  engineering mapped to ATT&CK (Sigma rules), and alerting discipline: **baseline before alert**,
  a named destination and reviewer for every detection, and source-health reported first (a dead
  source reads identically to "nothing happened").
- **Selection criteria:** tune to a reviewable alert volume — because true intrusions are rare, the
  false-alarm rate, not the detection rate, limits usefulness (the base-rate result). An ignored
  console is worse than none.
- **Anchor tools:** Wazuh (SIEM/XDR, detect); Falco (runtime, detect); osquery (endpoint
  visibility, detect); Suricata / Zeek (network detection sources); OpenSearch + Grafana / Loki /
  Prometheus (search/observability) — prefer **OpenSearch** over the Elastic Stack, which is
  SSPL/Elastic-License, not OSS; Sigma (detection rule format); Velociraptor (DFIR/endpoint,
  detect).
- **Maintenance:** tune to a reviewable volume; monitor source health.

### L7 — Resilience, backup & incident response
- **Development:** tested 3-2-1 backups (three copies, two media, one offline/immutable and
  encrypted), scheduled restore tests, ransomware resilience, incident-response runbooks written
  before they are needed (evidence collection in order of volatility), and forensic readiness.
- **Selection criteria:** the backup must be **restore-tested on a schedule** and versioned or
  immutable against ransomware; the IR runbook must exist before the incident.
- **Anchor tools:** restic / BorgBackup / Kopia / Duplicati / Velero (k8s) / pgBackRest / Barman
  (backup, recover); Velociraptor / GRR (DFIR, detect); MISP (threat-intel), Cortex (analysis),
  Timesketch (forensic timeline), Autopsy + The Sleuth Kit, YARA, CyberChef (forensic). Note:
  TheHive is no longer distributed as open source (since 2023) — use Cortex / Velociraptor.
- **Maintenance:** dated restore tests; runbook drills; a detection/hardening improvement after
  every incident.
<!-- AGENTTEAMS:END infra_security_layers -->

<!-- AGENTTEAMS:BEGIN infra_security_tool_catalog v=1 -->
## 3. Consolidated open-source tool catalog

**Currency stamp (binding).** Every entry was verified against its official repository on
**2026-08-22**. Licenses and open-source status **change** — HashiCorp Vault relicensed to BUSL,
Elastic to SSPL, TheHive left OSS — so **re-verify a tool's license before relying on it**, and
treat this table as a dated snapshot, not a standing guarantee. A tool's inclusion is not an
endorsement or a security claim; deployment and testing on the real target are what provide
security.

Control verbs: **detect** (observe/report) · **reactive-block** (act after an observation) ·
**inline-prevent** (refuse in-path) · **harden** (reduce attack surface) · **compliance-scan** ·
**recover**. Some tools carry more than one by deployment.

| Tool | License | Layer(s) | Verb |
|---|---|---|---|
| OpenSCAP | LGPL-2.1 | L0, L3 | compliance-scan |
| SCAP Security Guide (ComplianceAsCode) | BSD-3-Clause | L0, L3 | compliance-scan |
| Lynis | GPL-3.0 | L0, L3 | compliance-scan / audit |
| OPA | Apache-2.0 | L0 | inline-prevent (policy) |
| Conftest | Apache-2.0 | L0 | inline-prevent (policy) |
| Prowler | Apache-2.0 | L0 | detect (cloud posture) |
| ScoutSuite | GPL-2.0 | L0 | detect (cloud posture) |
| Cloud Custodian | Apache-2.0 | L0 | inline-prevent / detect (cloud policy) |
| Steampipe | AGPL-3.0 | L0 | detect (cloud posture) |
| Keycloak | Apache-2.0 | L1 | inline-prevent (IdP) |
| Authentik | MIT (core; EE proprietary) | L1 | inline-prevent (IdP) |
| Zitadel | AGPL-3.0 | L1 | inline-prevent (IdP) |
| Ory Hydra | Apache-2.0 | L1 | inline-prevent (OAuth2/OIDC) |
| Ory Kratos | Apache-2.0 | L1 | inline-prevent (identity) |
| Dex | Apache-2.0 | L1 | inline-prevent (OIDC broker) |
| Authelia | Apache-2.0 | L1 | inline-prevent (forward-auth) |
| oauth2-proxy | MIT | L1 | inline-prevent (forward-auth) |
| Vouch Proxy | MIT | L1 | inline-prevent (forward-auth) |
| OpenFGA | Apache-2.0 | L1 | inline-prevent (authz) |
| Casbin | Apache-2.0 | L1 | inline-prevent (authz) |
| step-ca (Smallstep) | Apache-2.0 | L2 | harden (PKI/ACME) |
| cert-manager | Apache-2.0 | L2 | harden (PKI/ACME) |
| Certbot | Apache-2.0 | L2 | harden (ACME) |
| OpenBao | MPL-2.0 | L2 | harden (secrets store) |
| Infisical | MIT (core; EE proprietary) | L2 | harden (secrets store) |
| SOPS | MPL-2.0 | L2 | harden (encrypt at rest) |
| age | BSD-3-Clause | L2 | harden (encrypt) |
| Sigstore cosign | Apache-2.0 | L2, L5 | inline-prevent (sign/verify) |
| gitleaks | MIT | L2, L5 | detect (secret scan) |
| trufflehog | AGPL-3.0 | L2, L5 | detect (secret scan) |
| osquery | Apache-2.0 (dual GPL-2.0) | L3, L6 | detect (telemetry) |
| AppArmor | GPL-2.0-or-later | L3 | inline-prevent (MAC) |
| SELinux | GPL-2.0 / LGPL-2.1 (per component) | L3 | inline-prevent (MAC) |
| firejail | GPL-2.0 | L3 | inline-prevent (sandbox) |
| bubblewrap | LGPL-2.0+ | L3 | inline-prevent (sandbox) |
| auditd | GPL-2.0 / LGPL-2.1 | L3 | detect (audit log) |
| Santa | Apache-2.0 | L3 | inline-prevent (binary auth, macOS) |
| Trivy | Apache-2.0 | L3, L5 | detect / compliance-scan |
| Docker Bench for Security | Apache-2.0 | L3 | compliance-scan |
| kube-bench | Apache-2.0 | L3 | compliance-scan |
| Falco | Apache-2.0 | L3, L6 | detect (runtime) |
| nftables / iptables | GPL-2.0 | L4 | inline-prevent (firewall) |
| pf | BSD/ISC | L4 | inline-prevent (firewall) |
| OPNsense | BSD-2-Clause | L4 | inline-prevent (firewall) |
| pfSense CE | Apache-2.0 (CE; Plus not OSS) | L4 | inline-prevent (firewall) |
| Suricata | GPL-2.0 | L4, L6 | detect (IDS) / inline-prevent (IPS) |
| Zeek | BSD-3-Clause | L4, L6 | detect (NSM) |
| Snort 3 | GPL-2.0 (engine + community rules) | L4 | detect (IDS) / inline-prevent (IPS) |
| CrowdSec | MIT | L4 | detect + reactive-block |
| Fail2ban | GPL-2.0-or-later | L4 | reactive-block |
| Pi-hole | EUPL-1.2 | L4 | inline-prevent (DNS filter) |
| AdGuard Home | GPL-3.0 | L4 | inline-prevent (DNS filter) |
| Unbound | BSD-3-Clause | L4 | harden (DNSSEC) |
| WireGuard | GPL-2.0 (kernel); tools MIT | L4 | harden (VPN) |
| nmap | NPSL (custom, non-OSI) | L4 | detect (audit/recon) |
| Semgrep | LGPL-2.1 (CLI; platform paid) | L5 | detect (SAST) |
| Bandit | Apache-2.0 | L5 | detect (SAST, Python) |
| OWASP ZAP | Apache-2.0 | L5 | detect (DAST) |
| Grype | Apache-2.0 | L5 | detect (SCA) |
| Syft | Apache-2.0 | L5 | detect (SBOM) |
| OSV-Scanner | Apache-2.0 | L5 | detect (SCA) |
| Dependency-Track | Apache-2.0 | L5 | detect (SCA/SBOM) |
| OWASP Dependency-Check | Apache-2.0 | L5 | detect (SCA) |
| pip-audit | Apache-2.0 | L5 | detect (SCA, Python) |
| in-toto | Apache-2.0 | L5 | inline-prevent (provenance) |
| slsa-github-generator | Apache-2.0 | L5 | inline-prevent (provenance) |
| cyclonedx-cli | Apache-2.0 | L5 | detect (SBOM) |
| OpenSSF Scorecard | Apache-2.0 | L5 | detect (repo posture) |
| Wazuh | GPL-2.0 | L6, L0 | detect (SIEM/XDR) |
| OpenSearch | Apache-2.0 | L6 | detect (log store/search) |
| Prometheus | Apache-2.0 | L6 | detect (metrics) |
| Grafana | AGPL-3.0 | L6 | detect (dashboards) |
| Grafana Loki | AGPL-3.0 | L6 | detect (log aggregation) |
| Sigma (SigmaHQ) | DRL-1.1 (rules) | L6 | detect (rule format) |
| Velociraptor | AGPL-3.0 | L6, L7 | detect (DFIR) |
| restic | BSD-2-Clause | L7 | recover (backup) |
| BorgBackup | BSD-3-Clause | L7 | recover (backup) |
| Kopia | Apache-2.0 | L7 | recover (backup) |
| Duplicati | MIT | L7 | recover (backup) |
| Velero | Apache-2.0 | L7 | recover (k8s backup) |
| pgBackRest | MIT | L7 | recover (Postgres backup) |
| Barman | GPL-3.0 | L7 | recover (Postgres backup) |
| GRR Rapid Response | Apache-2.0 | L7 | detect (DFIR) |
| MISP | AGPL-3.0 | L7 | detect (threat-intel) |
| Cortex | AGPL-3.0 | L7 | detect (analysis) |
| Timesketch | Apache-2.0 | L7 | detect (forensic timeline) |
| Autopsy / The Sleuth Kit | Apache-2.0 / multi | L7 | detect (forensic) |
| YARA | BSD-3-Clause | L7 | detect (hunting) |
| CyberChef | Apache-2.0 | L7 | detect (analysis) |

**Not open source (do not cite as such):** HashiCorp Vault (BUSL-1.1 → use OpenBao); Elastic Stack
(SSPL / Elastic License → use OpenSearch); Graylog (SSPL); CIS-CAT Pro (paid); pfSense Plus
(commercial); TheHive (left OSS in 2023 → use Cortex/Velociraptor). **AGPL copyleft** (open source,
but obligations for hosted/embedded use): Zitadel, trufflehog, Grafana, Loki, Velociraptor, MISP,
Cortex, Steampipe. **Non-standard:** nmap (NPSL), Sigma rules (DRL-1.1). **Bundled, not a
standalone tool:** `npm audit` (a subcommand of the npm CLI).
<!-- AGENTTEAMS:END infra_security_tool_catalog -->

<!-- AGENTTEAMS:BEGIN operational_integration v=1 -->
## 4. How this reference is used and kept current

- **Consumed by:** the producing / workstream agents that build the deployed system (they select
  and implement per-layer controls, weighted to the attack surface); `@technical-validator`
  (verifies a claimed control exists and engages on the target); `@security` (reviews a
  service-deploying project against this checklist — read-only, does not build).
- **Weighting, not completeness:** do not adopt all eight layers uniformly. Weight to the actual
  attack surface and adopt the highest assurance-per-effort controls first — for anything
  irreplaceable, a restore-tested backup (L7) caps the blast radius of every other failure.
- **Currency obligation:** the §3 table is a dated snapshot. Re-verify a tool's license and
  maintenance status before adopting it. A future enhancement may fold this catalog into the
  `security-vulnerability-watch` refresh pipeline so it is machine-checked rather than hand-dated.
- **Honest posture language:** record "engages as tested on LearnPythonStatsEcon's target," never
  "verified" or "secure." A control not deployed and tested provides no assurance.
<!-- AGENTTEAMS:END operational_integration -->

## 5. Project-specific infrastructure-security notes

<!-- Project-owned: record LearnPythonStatsEcon's chosen layers, tools, deviations, and rationale below.
     An infrastructure update leaves this section untouched (it is USER-EDITABLE). -->

_None recorded yet._
