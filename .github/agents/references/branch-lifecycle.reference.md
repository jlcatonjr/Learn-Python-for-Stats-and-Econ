<!--
SECTION MANIFEST
| section_id      | designation |
|-----------------|-------------|
| branch_lifecycle| FENCED      |
-->

<!-- AGENTTEAMS:BEGIN branch_lifecycle v=1 -->
# Branch Lifecycle Reference — LearnPythonStatsEcon

The procedure for what happens to a branch after its work lands: how every branch is classified,
what keeps one, and how one is deleted without losing work. `@git-operations` applies it after
every merge; `@cleanup` runs the periodic sweep. The executable form is
`agentteams --branch-inventory | --branch-cleanup | --branch-post-merge`; the manual command
sequence at the end is for projects without agentteams installed.

**Two rules decide everything.**

- **Deletion is never the test.** `git branch -d` checks against the upstream or `HEAD`, not the
  default branch, so it is a last guard only. "Merged" is decided first, by ancestry or by a
  verified merged PR.
- **Act only on the push remote** (normally `origin`), never on an upstream or a fork remote.

## 1. States

Classify each ref separately: a local branch with unpushed commits never inherits its remote
twin's state. Rules are evaluated in order, and the first match wins. *N* defaults to 14 days.

| # | State | Test | Action |
|---|---|---|---|
| 1 | Default | the default branch | Keep. Check that local equals the push remote. |
| 2 | Protected | branch protection or a ruleset covers it (API) | Keep. Never delete. |
| 3 | Evergreen / bot | named by a workflow `branch:` key (detected), or by a gate script (check by hand) | Keep. Reconcile its PR. |
| 4 | Release (maintained) | a declared maintained release line | Keep. |
| 5 | Release (finished) | matches the release pattern, and rule 6 or 7 holds | Tag `archive/<branch>` (annotated), confirm on the remote, then delete. |
| 6 | Merged | the tip is an ancestor of the default branch, and the branch owns at least one commit off the default branch's first-parent history (an empty fresh branch owns none); **or** an ancestor that owns no commits and has been idle more than *N* days (a fast-forward-merged or abandoned empty branch) | Delete. |
| 7 | Merged-by-PR | a PR whose head repository is the push remote's (never a fork with the same name), whose base is the default branch, is merged, whose `head.sha` equals this ref's tip (every PR with that head is checked), and whose merge commit is reachable from the default branch | Delete, after confirming `refs/pull/<n>/head` equals the tip on the remote. |
| 8 | Patch-equivalent | not rule 6 or 7, but `git cherry` shows 0 unique patches | **Not merged** (patch IDs ignore whitespace and skip merges). Ask the operator; archive-tag only on their answer. |
| 9 | Active | last activity within *N* days (includes empty fresh branches) | Keep. |
| 10 | Stale-unmerged | unique work, idle for more than *N* days | **Never auto-delete.** Offer the operator three choices: merge, rebase and continue, or archive then delete. |

**Why squash merges need rule 7.** A squash or rebase merge rewrites the commits, so the branch tip
is never an ancestor of the default branch. `git cherry` recognizes only a squash of a
*single-commit* branch, because it compares per-commit patch IDs. A Merged-by-PR branch's commits
are **not** reachable from the default branch, so its restore path is the GitHub-retained
`refs/pull/<n>/head`, which is why that ref is confirmed before every deletion.

**API results.** A 401, 403 or 404 on a list call, a rate limit, a network failure, or a missing
`gh` or token all mean **unknown**, never "no PR" or "not protected".

## 2. Holds

A hold overrides any action that rules 5–8 propose, including rule 8's archive tag. Record every
hold in the report.

- **Owner:** an author of the branch's own commits is not on the operator list. That list is
  `git config user.email` plus any `--operator-email`, and an unmatched author holds (fail
  closed). Delete only with the owner's consent, asked as one batched question.
- **Link:** a `tree/<branch>`, `blob/<branch>/` or `compare/…<branch>` URL appears in a tracked
  file, including correspondence already sent. Links sent outside the repository can't be found,
  so for a branch that was ever shared by link, tag it and repoint the links first.
- **Open PR:** the branch is the head **or the base** of an open PR, including PRs from forks.
- **Worktree:** it is checked out in a worktree. Prune a dead worktree record first
  (`git worktree prune`).
- **Pinned:** a workflow `ref:` or a submodule `branch =` pins it (both detected), or a lockfile
  pins it (check by hand).
- **Session:** another active session declares it as its working branch. The tool does not
  detect this, so check it by hand before any deletion.

## 3. Guards: every one is required

1. **Re-inventory immediately before acting.** Skip any ref whose tip or verdict drifted since the
   audit.
2. **Re-check each ref just before deleting it.** For an ancestry branch, check ancestry again. For
   a Merged-by-PR branch, re-query the PR, stop if `head.sha` moved, and confirm
   `git ls-remote <remote> refs/pull/<n>/head` equals the tip.
3. **Local refs** go first, while their upstream still exists:
   - ancestry: `git branch -d -- <b>`, **never `-D`**;
   - Merged-by-PR: the compare-and-delete `git update-ref -d refs/heads/<b> <sha>`, because `-d`
     would refuse a squash-merged branch.
4. **Remote refs,** one at a time:
   `git push <remote> --delete --force-with-lease=refs/heads/<b>:<audited-sha> refs/heads/<b>`
   (the full ref, so a tag with the same name is never touched).
5. **Tags** are created only when absent locally and on the remote, never moved, annotated, and
   confirmed with `git ls-remote --tags` before their branch is deleted.
6. **Stop at the first failure,** and never retry with force.
7. **If the open-PR hold cannot be checked,** no remote deletion runs at all.
8. **Record every deletion in the hash-chained `references/branch-deletions.log.csv`.** An
   `attempt` row is appended **before** the command runs, then a row with the outcome, the old
   SHA and the restore command.

**Restore:**
- remote: `git push <remote> <sha>:refs/heads/<b>`;
- Merged-by-PR: first `git fetch <remote> pull/<n>/head`, then the same push;
- local: `git branch <b> <sha>` (for a Merged-by-PR branch, run `git fetch <remote> pull/<n>/head`
  first).

## 4. Authorization (C-5 clearance precedes destruction; C-2 HALT is final)

| Mode | Covers | Authorization |
|---|---|---|
| `--branch-cleanup PLAN --apply` | any plan written by `--branch-inventory` (bulk, remote, Merged-by-PR, releases) | A `@security` **PASS** recorded **before** execution, for the action id `branch-cleanup:<the plan's full sha256>`. It covers exactly that plan, and the gate consumes it. |
| `--branch-post-merge <b> --apply` | only the branch whose tip is the **second parent** of the push remote's default-branch tip, which is the `--no-ff` merge just pushed; ancestry only, never rule 7 | An operator **Ed25519-signed, time-bounded `branch-delete` capability grant**, valid and not used up. One run (local plus remote ref) is one use. Without one: exit 3; use `--branch-cleanup` under a clearance. |

**Limits, stated plainly.**
- **The grant's real bound is `expires_at`, so keep it short.** `max_uses` is counted from the
  deletion ledger, whose hash chain has no key. A writer who removes the ledger resets the count,
  so treat `max_uses` as advisory.
- **The operator prompt is a speed-bump, not a boundary.** The runtime gate matches spellings, and
  other spellings can get past it.
- **The trust anchors come from the project's own team dir.** `--team-dir` accepts only
  `.claude/agents`, `.github/agents` or `.codex/agents` under the project, never an external
  path. The project itself, though, is whatever `--project` names. An agent that points it at a
  scratch clone of the same remote, with its own planted team dir, can satisfy the grant and
  clearance checks there. That gives it no more power than running `git push --delete` from that
  clone, which the runtime gate also only prompts on. In that case **the operator prompt is the
  only real control,** so read the `--project` path before approving an `--apply`.

- **HALT:** a `@security` HALT on `branch-delete` stops both modes.
- **Operator prompt:** both `--apply` forms are also routed to the operator by the runtime delete
  gate.
- **Grant provisioning:** the operator does this in an interactive shell, never in an agent
  session.
  1. Provision a signing key with `references/authorized-verify-keys/provision-operator-signing-key.sh`
     from an agentteams checkout.
  2. Name an approver in the team dir's `references/security-approvers.txt`. Keep `security` on
     that roster too, because it is also the decision-author roster.
  3. Sign a spec with `agentteams --sign-grant SPEC.json --framework <fw> --project <repo>`. Pass
     `--project`, not `--output`: the grant ledger must land at
     `<repo>/references/capability-grants.log.csv`, which is where `--branch-post-merge` reads it.
     The spec needs every field:
     - `"permitted_ops": "branch-delete"`;
     - `issuer_team` and `holder_team`, both set to the team id (the slug of the build log's
       `project_name`, or `--team-id`);
     - `target_path`: the absolute repository path;
     - a short `expires_at`;
     - `max_uses`;
     - `approver`, named on the roster;
     - `ticket_id` and `reason_code`;
     - `key_id`: the stem of the verify key's file name.
- An HMAC-signed `branch-delete` grant is refused, because the HMAC key is visible inside a
  sandbox.
- **When the workspace enforces signed decisions** (`references/agent-privilege.json`:
  `enforce_decision_signing: true`) and no decision key is provisioned, an unsigned PASS row cannot
  clear `--branch-cleanup`. Authenticate `@security`'s verdict with a C-2 security waiver
  instead. The operator, in their own shell:
  - mints one row in `references/security-waivers.log.csv` with `action_reviewed` set to
    `branch-cleanup:<plan sha256>`, `approver` set to `security`, `max_uses` set to 1 and a short
    `expires_at`;
  - signs it with a session-only `AGENTTEAMS_WAIVER_SIGNING_KEY`;
  - runs `--branch-cleanup <plan> --apply` in that same shell. The run consumes the waiver, and
    the key is never written down.

## 5. Cadence and reporting

- **After every merge to the default branch** (`@git-operations`):
  1. Merge with `--no-ff`. The merge commit's second parent is what records the branch tip; also
     name the branch in the message (`Merge branch '<b>'`) for readers.
  2. Push and pass the post-push CI/CD check.
  3. Run `agentteams --branch-post-merge <b>`. Add `--apply` when a grant exists; otherwise
     request clearance.
- **At close-out of a session that merged or pushed:** run `agentteams --branch-inventory` and
  report its summary line.
- **Weekly, or on request** (`@cleanup`): run
  `agentteams --branch-inventory --branch-report <dir>`, propose deletions by state, obtain
  clearance, then run `--branch-cleanup <dir>/branch-deletion-plan.json --apply`.
- **Several machines:** the inventory sees only this machine's local branches and the push remote.
  Say so, and ask the operator to run it on every machine that holds local work.
- **Output Contract fields:**
  - `Branch disposition: deleted (local and remote, old SHA) | kept — hold: <reason>`
  - `Branch inventory: clean | N merged-undeleted | N patch-equivalent | N stale-unmerged`
- **GitHub setting:** for PR workflows, also turn on "Automatically delete head branches"
  (`delete_branch_on_merge`). Local merges never trigger it, so it complements this procedure and
  doesn't replace it.

## 6. Manual sequence (no agentteams)

```bash
git fetch --prune origin; D=refs/remotes/origin/main
for b in $(git for-each-ref --format='%(refname:short)' refs/heads); do echo "$b ancestor=$(git merge-base --is-ancestor "$b" $D && echo yes || echo no) unique=$(git cherry $D "$b" | grep -c '^+') behind/ahead=$(git rev-list --left-right --count $D..."$b" | tr '\t' /)"; done
gh pr list --state open --json number,headRefName,baseRefName   # open-PR holds
```

Apply §1–§3 by hand to that output. Every bulk or remote deletion still needs its recorded
clearance first.
<!-- AGENTTEAMS:END branch_lifecycle -->
