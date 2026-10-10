#!/usr/bin/env bash
# ============================================================================================
# dedicated-uid-provisioning.example.sh  -  INERT EXAMPLE. DO NOT RUN. DOES NOT ELEVATE.
# ============================================================================================
# This file is a REFERENCE ONLY, shipped alongside confine-run.sh as documentation for TIER-B
# (operator-provisioned, out-of-band) isolation. It is NEVER auto-run by the launcher and it
# NEVER calls sudo/dscl itself in this file - every privileged line below is COMMENTED OUT and
# guarded by an unconditional early exit. An operator performs these steps MANUALLY, out of band,
# on a box they own, after their own review.
#
# WHY A DEDICATED UID:
#   confine-run.sh's --nproc-max maps to RLIMIT_NPROC, which the macOS/BSD kernel enforces
#   PER-UID, not per-process-tree. It therefore bounds a *tenant* only if that tenant's launcher
#   is ALREADY running as its own uid with no other processes. On a shared login uid the limit
#   counts every process the human owns -> it is a self-DoS knob, not isolation.
#
#   confine-run.sh deliberately does NOT drop uid itself: doing so would make the launcher
#   root-requiring and turn attacker-influenced argv into a privilege-escalation surface (audit
#   finding 3, plan section 2). Instead the operator LAUNCHES the whole confine-run.sh already running as
#   the dedicated uid (e.g. `sudo -u _agenttenant1 confine-run.sh ...` from a trusted context).
#
# This mirrors how egress-netns-wiring.sh is an OOB root step on Linux - provisioning is OOB here too.
# ============================================================================================
echo "dedicated-uid-provisioning.example.sh is INERT reference documentation. Nothing was executed." >&2
echo "Read it, adapt it, run the steps MANUALLY and deliberately as an operator. Exiting 0." >&2
exit 0

# ---- BELOW THIS LINE IS UNREACHABLE (post-exit) REFERENCE ONLY -----------------------------
#
# TENANT="_agenttenant1"          # macOS service accounts conventionally start with an underscore
# TENANT_UID=601                  # pick an unused uid; verify with: dscl . -list /Users UniqueID
# TENANT_GID=601
#
# # 1) Create a hidden service group + user (macOS uses dscl, not useradd). ALL require root.
# # sudo dscl . -create /Groups/$TENANT
# # sudo dscl . -create /Groups/$TENANT PrimaryGroupID $TENANT_GID
# # sudo dscl . -create /Users/$TENANT
# # sudo dscl . -create /Users/$TENANT UniqueID $TENANT_UID
# # sudo dscl . -create /Users/$TENANT PrimaryGroupID $TENANT_GID
# # sudo dscl . -create /Users/$TENANT UserShell /usr/bin/false      # no interactive login
# # sudo dscl . -create /Users/$TENANT NFSHomeDirectory /var/empty   # no home
# # sudo dscl . -create /Users/$TENANT IsHidden 1
# #
# # 2) Give it ONLY its per-tenant scratch (never the operator's files).
# # sudo mkdir -p /var/agent-tenants/$TENANT/scratch
# # sudo chown -R $TENANT_UID:$TENANT_GID /var/agent-tenants/$TENANT
# #
# # 3) Launch confine-run.sh ALREADY as that uid (the launcher itself never drops privilege):
# # sudo -u $TENANT /path/to/confine-run.sh \
# #     --scratch /var/agent-tenants/$TENANT/scratch \
# #     --egress proxy --proxy 127.0.0.1:8443 \      # loopback proxy - see confine-run.sh notes
# #     --cpu-max 60 --nproc-max 64 \                # now RLIMIT_NPROC actually bounds THIS tenant
# #     -- <agent command>
# #
# # RESIDUALS (honest): a dedicated uid is COARSER than a Linux netns/cgroup tenant. It shares the
# # host kernel and global namespaces; RLIMIT_NPROC is a count, not a cgroup pids controller; and
# # per-tenant network isolation still needs the PF anchor (see pf-per-tenant-anchor.example.conf),
# # which is root and churns on network changes. Durable multi-tenant isolation remains Layer B
# # (VM/container) or a Linux host.
