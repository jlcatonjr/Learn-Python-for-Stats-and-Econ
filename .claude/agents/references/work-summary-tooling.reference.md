<!-- AGENTTEAMS:BEGIN content v=1 -->
# Work Summary Tooling Reference

## Daily Window Commands

Set target date:
- `DATE=YYYY-MM-DD`

List commits in window:
- `git log --since="$DATE 00:00" --until="$DATE 23:59" --pretty=format:'%h|%ad|%s' --date=iso`

Show commit stats/diff:
- `git show --stat <hash>`
- `git show <hash> -- <path>`

List plan artifacts:
- `ls -1 tmp/by-week/*/*.plan.md tmp/by-week/*/*.steps.csv`
- `ls -1 tmp/*.plan.md tmp/*.steps.csv`

Validate commit hash:
- `git cat-file -e <hash>`

## Weekly Synthesis Commands

Set target ISO week:
- `WEEK=YYYY-Www`

List daily summaries:
- `ls -1 workSummaries/daily/*.md`

Optional preflight organizer when the project provides one:
- Run the repository's week-organization helper if it exists.

Read daily summaries:
- `sed -n '1,220p' workSummaries/daily/YYYY-MM-DD.md`

## Monthly Synthesis Commands

Set target month:
- `MONTH=YYYY-MM`

List weekly summaries:
- `ls -1 workSummaries/weekly/YYYY-W*.md`

Read weekly summaries:
- `sed -n '1,260p' workSummaries/weekly/YYYY-Www.md`

## Correlation Heuristics

When associating commits with plans, prioritize:
1. Plan slug in commit message
2. File overlap between commit diff and `outputs` column in `tmp/by-week/YYYY-Www/<slug>.steps.csv` or legacy `tmp/<slug>.steps.csv`
3. Time adjacency between commit time and step status changes

If no criterion matches, classify under **Other Transformations**.

## Guardrails

- Never fabricate links between commits and plans.
- Never delete existing summaries without explicit instruction.
- Default to `append` for same-day completion capture when a daily file already exists.
- Exclude `.github/agents/.agentteams-backups/` from evidence collection unless the request is explicitly forensic.
- Keep summary generation scoped to this repository.
- Run required adversarial and conflict audits after summary generation.
<!-- AGENTTEAMS:END content -->
