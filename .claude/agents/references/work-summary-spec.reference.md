<!-- AGENTTEAMS:BEGIN content v=1 -->
# Work Summary Spec

## Purpose

Define the required evidence model, structure, and acceptance criteria for work summaries in this repository.

## Output Paths

- Daily: `workSummaries/daily/YYYY-MM-DD.md`
- Weekly: `workSummaries/weekly/YYYY-Www.md`
- Monthly: `workSummaries/monthly/YYYY-MM.md`

## Evidence Classes

Only two source classes are allowed:
1. Planning artifacts in canonical `tmp/by-week/YYYY-Www/` storage plus legacy undated artifacts in `tmp/` (`*.plan.md`, `*.steps.csv`)
2. Git history from this repository (metadata + diffs)

## Authoritative Boundaries

- Git history is authoritative for what changed.
- Plan artifacts are authoritative for intended sequence and declared statuses.
- If they disagree, report the mismatch in a **Discrepancies** section.

## Daily Summary Minimum Requirements

1. Date window in local time
2. Machine-parseable fields for date, window start/end, commit count, plans touched count, and files changed count
3. Explicit write mode when updating an existing same-day file (`create`, `append`, or `replace`)
4. Plans touched in the window
5. Plan implementation outcomes
6. Other transformations not clearly plan-linked
7. Discrepancies
8. Open items at end of day
9. Source section naming planning artifacts and commit range

## Weekly Summary Minimum Requirements

1. Derived from daily summaries for target ISO week
2. Number of daily files consumed and expected
3. Machine-parseable fields for plans touched/completed/blocked and coverage status
4. Grouped plans: completed / in-progress / blocked
5. Aggregated discrepancies
6. Missing-daily handling statement
7. Direct links to planning artifacts in `tmp/by-week/YYYY-Www/` when present, falling back to legacy `tmp/`

## Monthly Summary Minimum Requirements

1. Derived from weekly summaries for target month
2. Number of weekly files consumed and expected
3. Machine-parseable fields for coverage status and missing-weekly list
4. Direct links to consumed weekly summaries
5. Missing-week handling statement
6. Aggregated carry-over discrepancies

## Evidence Handling Rules

1. Treat `tmp/by-week/YYYY-Www/` as canonical when present; use undated `tmp/` artifacts as fallback or carry-over inputs
2. Exclude `.github/agents/.agentteams-backups/` from git-activity collection unless the request is explicitly forensic
3. If the repository provides a helper to organize `tmp/` by week, run it before weekly/monthly synthesis; otherwise continue with existing on-disk organization

## Audit Requirements

After each generated summary:
1. `@technical-validator` for daily summaries
2. `@adversarial`
3. `@conflict-auditor`

For weekly output, also run aggregate weekly-batch audits over all weekly files.
<!-- AGENTTEAMS:END content -->
