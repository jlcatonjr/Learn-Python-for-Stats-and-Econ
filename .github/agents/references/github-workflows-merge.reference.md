<!-- AGENTTEAMS:BEGIN content v=1 -->
# GitHub Workflows and Merge Strategy Reference

This reference defines safe GitHub interaction and merge procedures for LearnPythonStatsEcon.

## Official Sources

- About Git: https://docs.github.com/en/get-started/using-git/about-git
- About pull requests: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-with-pull-requests/about-pull-requests
- About pull request merges: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/incorporating-changes-from-a-pull-request/about-pull-request-merges
- Merge methods on GitHub: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/about-merge-methods-on-github
- Resolving merge conflicts on GitHub: https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/addressing-merge-conflicts/resolving-a-merge-conflict-on-github
- About protected branches: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- About rulesets: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
- About required status checks: https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-required-status-checks

## Merge Strategy Matrix

| Strategy | Use When | Risk Profile | Required Checks |
|---|---|---|---|
| Merge commit | Preserve full branch history | Medium (history noise) | CI green, reviewer approval, branch protections satisfied |
| Squash merge | Keep linear and compact history | Low/Medium (context compression) | CI green, PR description captures scope |
| Rebase merge | Keep linear history and individual commits | Medium/High (history rewrite complexity) | CI green, no policy conflict with branch/rulesets |
| Fast-forward (local) | Branch is directly ahead with no divergence | Low | Verify no hidden divergence (`git fetch`, compare refs) |

## Careful Merge Protocol

1. Confirm branch and ruleset constraints before selecting merge method.
2. Verify required status checks are passing.
3. Confirm review requirements and approval state are satisfied.
4. Check for merge conflicts and resolve using GitHub or local workflow as appropriate.
5. Complete merge according to project policy (merge/squash/rebase).
6. Run post-merge verification — including **CI/CD deployment verification** (see the next section) when the push/merge triggers Actions — and document noteworthy decisions for auditability.

## Post-Merge / Post-Push CI/CD Deployment Verification

**Distinct from pre-merge required status checks** (which *gate* the merge, above): this verifies the GitHub Actions runs that the push/merge itself **triggers** on the target branch — CI **and** deployment workflows (Pages, release, container/package publish, environment deploys). Those runs only come into existence *after* the ref updates, so a green pre-merge PR does not imply a green deployment.

**Applies only when** the operation pushed or merged to a branch, **and** the repository has workflows (`.github/workflows/*.yml`), **and** run status is reachable (the GitHub REST API, or `gh` if installed and authenticated). Otherwise skip and record `N/A`.

**Tooling preference — prefer `git` and the REST API over `gh`.** Use the `git` CLI for all ref/SHA/push work and the GitHub REST API (`curl https://api.github.com/...`) to read run status. `gh` is an *optional convenience* that is frequently **absent or unauthenticated** (headless CI, cron, minimal/sandboxed environments), so never make verification *depend* on it — the `gh` forms below are parenthetical fallbacks for when it happens to be installed. Likewise prefer `git push` over any `gh`-mediated push; when an HTTPS remote has no stored credentials, an SSH remote (`git@github.com:<owner>/<repo>.git`) often still authenticates.

**Procedure:**

1. **Identify the target and the pushed commit with `git`:** `git rev-parse HEAD` (the SHA whose runs you must verify) and `git remote get-url origin` (→ `<owner>/<repo>`).
2. **Find the triggered run(s)** for that commit on the target branch — expect roughly one run per workflow (e.g. a CI run *and* a deploy run):
   - REST: `curl -s "https://api.github.com/repos/<owner>/<repo>/actions/runs?per_page=20"`, then select the entries whose `head_sha` matches the pushed commit and record each run's `id`, `name`, `status`, `conclusion`.
   - (`gh` fallback: `gh run list --branch <branch> --limit 10`.)
3. **Wait for completion** and read the verdict — do not declare the operation done while a run is `queued`/`in_progress`:
   - REST: poll `curl -s "https://api.github.com/repos/<owner>/<repo>/actions/runs/<run-id>"` until `.status == "completed"`, then require `.conclusion == "success"`.
   - (`gh` fallback: `gh run view <run-id> --json status,conclusion,jobs`; `gh run watch <run-id>` blocks until completion when interactive.)
4. **On `failure`/`cancelled`/`timed_out`:**
   - Identify the failing step(s): REST `curl -s "https://api.github.com/repos/<owner>/<repo>/actions/runs/<run-id>/jobs"` → the `jobs[].steps[]` whose `conclusion` is `failure` (full logs need an authenticated token: `curl -H "Authorization: Bearer $GITHUB_TOKEN" .../actions/runs/<run-id>/logs` returns a zip). (`gh` fallback: `gh run view <run-id> --log-failed`.) Diagnose the root cause.
   - Fix the cause (code, config, or workflow), commit, and re-push with `git push`; the new push triggers a fresh run — re-verify from step 1. Iterate until green.
   - Re-run **only** for a confirmed transient/infrastructure flake, never to mask a real failure: re-push, or `gh run rerun <run-id>` (`--failed`) / REST `curl -X POST -H "Authorization: Bearer $GITHUB_TOKEN" .../actions/runs/<run-id>/rerun` when available.
   - Escalate to the orchestrator / `@security` if the fix is risky, ambiguous, or out of scope. **Deployment** workflow success (Pages/release/publish) is the binding outcome — a failed deploy means the change is not live and the operation is **not complete**.
5. **Cross-repo guard:** if a fix requires pushing to a repository other than `Textbook/`, that re-push is a cross-repository write — route it through `@repo-liaison` + `@security` (orchestrator Rule 11) before pushing.

## Conflict Handling Decision Tree

1. If conflict is simple and fully represented in changed files, resolve in GitHub UI.
2. If conflict spans generated files, templates, or multi-step refactors, resolve locally with full test and lint checks.
3. If conflict resolution changes architecture or policies, route through orchestrator + adversarial + conflict-auditor before final merge.

## Audit Logging Requirements

For each merge or rebase event, record:

- Source branch and target branch
- Merge method selected and rationale
- Conflict status (none / resolved in UI / resolved locally)
- Required status check snapshot (pass/fail) — the pre-merge gating checks
- Triggered CI/CD run id + conclusion (the post-merge deployment run, `success`/`failure`, or `N/A — no workflows`)
- Resulting commit hash(es)

These records support ex-post audit and incident reconstruction.
<!-- AGENTTEAMS:END content -->
