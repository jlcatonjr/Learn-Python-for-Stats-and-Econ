<!-- AGENTTEAMS:BEGIN content v=1 -->
# authorized-verify-keys

This directory holds the operator-provisioned Ed25519 public verify keys for
decision signing, one `<key-id>.pub.pem` file per key. The operator provisions
keys OUTSIDE any agent sandbox.

When the team is sandboxed (confined/exclusive), this directory is write-denied
to in-sandbox agents so an agent cannot plant its own key. agentteams emits only
this README (so the denied path always exists) and never writes, rewrites or
deletes any `*.pub.pem` file here.
<!-- AGENTTEAMS:END content -->
