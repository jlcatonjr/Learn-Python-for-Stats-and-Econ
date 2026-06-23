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
6. Run post-merge verification and document noteworthy decisions for auditability.

## Conflict Handling Decision Tree

1. If conflict is simple and fully represented in changed files, resolve in GitHub UI.
2. If conflict spans generated files, templates, or multi-step refactors, resolve locally with full test and lint checks.
3. If conflict resolution changes architecture or policies, route through orchestrator + adversarial + conflict-auditor before final merge.

## Audit Logging Requirements

For each merge or rebase event, record:

- Source branch and target branch
- Merge method selected and rationale
- Conflict status (none / resolved in UI / resolved locally)
- Required status check snapshot (pass/fail)
- Resulting commit hash(es)

These records support ex-post audit and incident reconstruction.
<!-- AGENTTEAMS:END content -->
