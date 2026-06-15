<!-- AGENTTEAMS:BEGIN content v=1 -->
# Work Summary Backfill Reference — LearnPythonStatsEcon

<!-- agentteams-lint: no-memory-index OK -->
<!-- The phrases "git history of" and "previously adjudicated" below are incidental
     prose, not the memory-index consultation protocol. The one intentional
     memory-index pointer (Step 2, honor-prior-skips) is a guidance reference, not
     an agent consultation step, so the canonical memory_index_consultation fence
     does not apply to this reference document. -->

## Purpose

Strategy for **retroactively filling whole-day gaps** in `workSummaries/daily/` (and, by extension,
missing weekly/monthly files). This covers **work-summary** backfill only (distinct from any
database/metadata backfill the project may have).

Backfill is a specialization of the `work-summarizer` daily workflow run for **past** dates whose daily
file is absent. The evidence model, contract fields, templates, and audit obligations are unchanged from
`work-summary-spec.reference.md` and `work-summary-templates.reference.md`; this document adds the
gap-analysis, adjudication, and date-attribution rules that backfill specifically needs.

## When To Use

- A user asks to "review missing work summaries and backfill," "fill the gaps," or names specific missing days.
- A weekly/monthly synthesis discovers missing daily files in its window and the user opts to fill them
  (in-synthesis weekly/monthly gap-fill stays user-gated).
- **Automatically, at session close** — the *Automatic Trigger* (below) detects recent past
  active-day daily gaps and runs this backfill workflow without an explicit request. Daily backfill
  is therefore **no longer request-only**: it happens on request **or** via the automatic sweep.
  (Weekly/monthly in-synthesis gap-fill remains user-gated — the automatic sweep is daily-only.)

## Automatic Trigger (session-close sweep)

> **Single source of truth.** This section is the authoritative definition of the automatic
> past-day backfill trigger. The orchestrator's *Past-Day Backfill Obligation* rule, the
> orchestrator closeout step that invokes it, and the work-summarizer's *Workflow D — Automatic
> Backfill Sweep* all **point here** for semantics and must not restate the window, the cap, or the
> Rule-12 partition (avoids same-fact-in-many-places drift; living-document policy).

**Why automatic.** The today-capture obligation (orchestrator Constitutional Rule 12 / the closeout
today-capture step) only records *today's* executed work; skipped *past* active days otherwise
accumulate silently until a human asks for a weekly summary or an explicit backfill. The automatic
sweep closes that gap.

**Named constant.** `AUTO_BACKFILL_LOOKBACK_CAP_DAYS` — the maximum age (in calendar days) the
automatic sweep will reach back to **auto-author**. Default **14**. Defined here once; every other
surface references the name, never the literal.

**Canonical clock.** All date math uses **git author-date in the repo-local timezone**, computed
once at session close. "Today" = the current local date.

**Partition with Rule 12 (disjoint + exhaustive).** Rule 12 owns **exactly today**. The automatic
sweep owns **strictly-prior active dates**, from `yesterday` back to `AUTO_BACKFILL_LOOKBACK_CAP_DAYS`.
**Today is never an automatic-backfill target.** No date is claimed by both rules or by neither.

**Trigger conditions (all must hold).**
1. **Executed-work gate** — the session executed work (commits, applied scripts/migrations, data
   mutations, or adjacent-repo activity — the same predicate Rule 12 uses). Read-only/query
   sessions skip detection entirely (zero overhead).
2. A gap is actually detected by Step 1 gap analysis (no gap → no work).

**Window.** `[latest_on_file_daily_date + 1 day, yesterday]`, capped to the most recent
`AUTO_BACKFILL_LOOKBACK_CAP_DAYS` days. Run Step 1–Step 7 of this reference over that window.

**Scope — create-only.** The sweep auto-authors **absent** active days in **`create` mode only**.
It does **NOT** auto-repair on-file-but-incomplete dailies (the Step 5 `append` case stays
user-requested). This keeps the idempotency guarantee ("on file → no longer a gap") sound.

**Honor prior skips — fail safe.** Apply Step 2 (honor prior adjudications). **Never auto-author a
day previously adjudicated `skip`.** If the skip source of truth (prior backfill plans /
memory-index) is absent or unreadable, **do not author — surface for human decision** (fail safe,
not fail open).

**Idempotency & no re-entrancy.** `create` mode + "on file → no longer a gap" makes repeated
same-day sessions safe and non-duplicating. The sweep fires **only from the orchestrator
session-close closeout (the past-day backfill step)**, runs **at most once per session**, and the
`@adversarial` / `@conflict-auditor` sub-sessions invoked inside Workflow D do **not** themselves
re-trigger it (they are leaf audit agents, not orchestrator session-close). No recursion.

**Edge cases.**
- Empty `daily/` folder → no `latest_on_file`; window lower bound = the cap only.
- `latest_on_file` in the future (mis-date / clock skew) → anomaly: surface, do **not** author.
- Inverted / empty window → no-op.
- Gap **older** than `AUTO_BACKFILL_LOOKBACK_CAP_DAYS` → **recommend-only**: surface a one-line
  notice (e.g. "N active days beyond the auto-backfill cap are un-summarized — run an explicit
  backfill"); never auto-author the overflow. The notice repeats on every executed-work close
  until the gap is filled — an intended forcing function, not a bug.

**Audit gate (single definition).** The backfilled set passes **Step 7** (adversarial → conflict);
below-PASS findings **block close and are surfaced to the user** (not silently self-remediated).
Workflow D and the orchestrator rule reference Step 7 and must not specify a divergent gate.

**Surfacing.** Report to the user: days auto-backfilled, days skipped (inactive / honored-skip),
and any overflow deferred as recommend-only.

## Core Rule — One Summary Per *Active* Day (not per calendar day)

**"One file per active day."** A missing date is **not** automatically a gap. A day with **0 commits
and no real same-day artifacts is intentionally skipped** — do not author an empty or speculative
summary for it.

**Gap = a date with no daily file that had real activity.** "Real activity" = at least one of:
- ≥1 commit in this repo authored that day (after excluding `.github/agents/.agentteams-backups/**`), OR
- genuine same-day execution/planning artifacts (plan/steps with that **work-date**, apply-logs, results,
  operation/deletion summaries — see the daily-completeness scan below).

## Step 1 — Gap Analysis

Enumerate on-file dailies vs per-day commit activity across the window:

```bash
# on-file dailies
ls -1 workSummaries/daily/*.md
# commits per local day (authoritative activity signal)
git log --since="<start> 00:00" --until="<end> 23:59" \
  --pretty=format:'%ad' --date=format:'%Y-%m-%d' | sort | uniq -c
```

Build a verdict table (the canonical, audited output shape):

| Day | Commits | Daily on file? | Same-day artifacts | Verdict |
|-----|--------:|----------------|--------------------|---------|
| ... | N       | yes/no         | count + note       | covered / **BACKFILL** / skip |

Verdict logic:
- on file → **covered** (do not touch; append only if materially incomplete — see Step 5).
- not on file + real activity → **BACKFILL**.
- not on file + 0 commits + no genuine artifacts → **skip** (record why).
- today / in-progress day → **skip** (not a historical gap) unless explicitly requested.

## Step 2 — Honor Prior Adjudications (don't re-litigate)

Earlier backfill runs may already have adjudicated some zero-activity days as **skip**. Treat those
decisions as authoritative; re-confirm cheaply (e.g. `git log` for the day = 0) but do not reopen them.
Query the memory-index / prior backfill plans first. **If the skip source of truth is absent or
unreadable, do not auto-author — surface for human decision (fail safe).**

## Step 3 — Date Attribution (the backfill-specific hazard)

The work-date of an artifact is **not** reliably its filesystem mtime. Resolve the true work-date by
**precedence**:

1. **Git author-date** of commits (authoritative for what changed, and the daily window boundary).
2. **Filename date** (`*-YYYY-MM-DD.*`) — a strong work-date signal for plan/doc artifacts.
3. **Content header date** ("**Date:** YYYY-MM-DD" inside the plan/doc).
4. **mtime** — *last resort only*; frequently wrong.

Known traps (recast generically):
- **Bulk-checkout mtimes.** A whole `tmp/by-week/` bucket can share one checkout mtime, so mtime tells
  you nothing about the work-date. Use filename/content/commit instead.
- **Next-day commit.** Work done on day D is sometimes committed on D+1 (often folded into an unrelated
  bulk commit). Attribute it to **D** (filename/content date), and add a **Discrepancy** note naming the
  next-day commit hash. **Cross-check the adjacent daily to prevent double-counting** (the D+1 daily must
  not also claim that work).
- **Date-stamped-but-uncommitted.** A `*-D.plan.md` may be prep authored before D or committed after D.
  Record `Linked commits: (none on D)` for the uncommitted ones and note it in Discrepancies.

## Step 4 — Evidence Model (unchanged + the daily-completeness scan)

Two authoritative classes only: (1) git history of this repo; (2) plan artifacts in
`tmp/by-week/YYYY-Www/` (+ legacy `tmp/`). For backfill, **always run the daily-completeness scan** so a
low/zero-commit day is not mis-portrayed as planning-only:

- Scan same-day execution-evidence (`*results*.md`, `*SUMMARY*.md`, apply-logs, rollback CSVs) as
  **corroborating, non-authoritative** context, and surface adjacent-repo commits as out-of-repo.
- A zero-commit day is **not** proof of a planning-only day — and a planning-heavy day must not be dressed
  up as execution. Mark blocked/held/gated items as such.
- **Cross-repo commit hashes** are allowed only when clearly bracketed as out-of-repo — they will not
  resolve via `git cat-file -e` in this repo, and that is correct.

## Step 5 — Author (create-mode; append for incomplete existing dailies)

- **Backfilled gap days:** `create` mode. Never overwrite an existing same-day file.
- **Existing-but-incomplete daily:** `append` a new session block (append-first rule). Use this when a day
  is on file but omits in-window commits. *(Append is user-requested; the automatic sweep is create-only.)*
- Match the canonical daily template and **all six contract fields** (`Date`, `Window Start`, `Window End`,
  `Commits Count`, `Plans Touched Count`, `Files Changed Count`).
- For a fan-out (several gap days at once), one agent per day is effective — each gathers its own git +
  artifact evidence and writes its file under the strict no-fabrication rules.

## Step 6 — Validation Gate (mechanical, before audit)

```bash
# every cited in-repo hash resolves
git rev-parse --verify -q "<hash>^{commit}"        # cross-repo hashes are expected to fail → must be labeled
# every cited local path exists; all six contract fields present; markdown links resolve
```

- `Commits Count` = git **author-date** count for the day (not a two-dot `A..B` range count — a branchy
  day makes `first..last` undercount and excludes off-line commits; state the author-date figure instead).
- `Files Changed Count` = distinct files touched in-window (raw git metric); routine `chore: index` /
  agent-infrastructure refreshes are normal and counted, but `.agentteams-backups/**` churn is excluded.

## Step 7 — Mandatory Audit Pass

Run **adversarial** then **conflict** audits over the backfilled set. Remediate every finding below PASS
**before** marking the run complete; record verdicts + remediations in the backfill plan's "Audit Result"
section. Below-PASS findings **block close and are surfaced to the user** (not silently self-remediated).

## Failure Modes To Avoid

| Failure | Prevention |
|---|---|
| Authoring a summary for a genuinely inactive day | Require real activity (commits or genuine same-day artifacts); honor prior skip decisions |
| Trusting mtime as work-date | Use git author-date / filename / content header; mtime last |
| Under-reporting a day whose work was committed next-day | Attribute by work-date; add Discrepancy + cross-check the adjacent daily for double-count |
| Double-counting across adjacent dailies | Verify the neighbor daily does not already claim the same commit/work |
| Portraying a planning day as execution (or vice-versa) | Daily-completeness scan; mark blocked/held/gated explicitly |
| `A..B` range mis-count on a branchy day | Report the author-date commit count, not a two-dot range |
| Fabricated/unresolvable hashes or paths | Validate every hash + path; bracket cross-repo hashes as out-of-repo |
| Skipping the audit pass | Adversarial + conflict are mandatory; remediate before close |
| Auto-authoring a day prior runs adjudicated `skip` | Honor prior skips; fail safe when the skip source is unreadable |

## Related References

- `work-summary-spec.reference.md` — evidence model, contract fields, acceptance criteria.
- `work-summary-templates.reference.md` — daily/weekly/monthly templates.
- `work-summary-tooling.reference.md` — `git log`/`git show` recipes and week-organization helper.
- `@work-summarizer` — the agent that owns this workflow (*Workflow D — Automatic Backfill Sweep*).
<!-- AGENTTEAMS:END content -->
