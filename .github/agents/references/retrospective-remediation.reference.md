<!-- AGENTTEAMS:BEGIN content v=1 -->
# Post-Deliverable Retrospective Reference — LearnPythonStatsEcon

## Purpose

Full semantics for the **Post-Deliverable Retrospective** subroutine (`@orchestrator`, invoked
from Workflow 1, Workflow 2, and Workflow 3's corrections-made branch). The orchestrator's rule
and workflow text intentionally stay terse and **point here** for the operative detail — avoids
same-fact-in-many-places drift (living-document policy).

The subroutine produces two audited, disjoint lists from one just-completed deliverable session:
1. **Repository-infrastructure lessons** — applied in-repo via `@agent-updater`. Not logged
   anywhere; the applied change *is* the record.
2. **AgentTeamsModule remediation items** — logged to a durable CSV so they outlive the session,
   since this project cannot write directly into the separate AgentTeamsModule repository.

## When This Runs

See the subroutine's own "Applies to" line for the exact trigger surface (Workflow 1, Workflow 2,
Workflow 3's corrections-made branch; explicitly not Workflow 4 or Workflows 5–10) and its
reachability clause (fires for ad-hoc sessions too). Not restated here.

## Category Definitions

### (a) Repository-infrastructure lesson

A **generalizable** gap in *this project's own* agent docs, rules, workflows, or routing that this
session's work exposed — something that would recur for the next similar request if left
unaddressed.

**Qualifies:**
- The session had to route around a missing rule or an ambiguous handoff (e.g., two agents both
  plausibly owned a task and the routing table didn't disambiguate).
- A workflow step referenced a file/path convention that turned out not to match this project's
  actual layout.
- An agent's Invariant Core was silent on a case this session had to improvise a decision for.

**Does not qualify:**
- A one-off content fix with no structural implication ("this docstring was out of date").
- Something already covered by an existing rule that the session simply followed correctly.
- A preference call with no right answer (that's a judgment call, not an infrastructure gap).

### (b) AgentTeamsModule remediation item

A gap in the **agentteams tool itself** — the template library, the `analyze`/`render`/`emit`
pipeline, `agentteams --update`/`--init` behavior, schemas, or CLI — that this session's work
exposed. The touch point is something a future `agentteams` maintainer would fix, not something
fixable inside this project alone.

**Qualifies:**
- A generated template's prose assumed something that isn't true for every project shape (a
  placeholder that doesn't resolve cleanly for a given project layout).
- A CLI flag or pipeline step produced a surprising or silently-wrong result under conditions this
  session actually hit.
- A cross-cutting mechanism (e.g. a liaison-log destination, a fence-propagation assumption) turned
  out to have a hidden assumption that broke for this project's specific setup.

**Does not qualify:**
- Anything specific to this project's own content with no implication for the generator.
- A feature request with no concrete triggering incident from this session (speculative
  "wouldn't it be nice if" items dilute the log's signal — skip them).

When in doubt, prefer silence: an empty retrospective is the expected, common case, not a failure
to look hard enough.

## Dedup Rule

Before appending any (b) item, read the existing remediation log (see Destination, below) and skip
any item whose normalized `summary` (lowercased, whitespace-collapsed) matches an existing `open`
row. `@conflict-auditor` performs this check once, in the subroutine itself; `@repo-liaison`'s
Protocol 5 re-checks as defense-in-depth, not as a second independent audit.

## Content-Safety Rule

Before appending, reject or sanitize (never append verbatim) any (b) item whose `summary` or
`proposed_touch_points` text:
- begins with a formula-injection character (`=`, `+`, `-`, `@`) — CSV/spreadsheet injection risk
  once this file is opened in a spreadsheet tool; prefix with a single quote or rewrite the
  sentence to not lead with that character, or
- reads as credential-like or secret-like content (tokens, keys, connection strings).

Escalate to `@security` only for that specific case — this keeps the common path (an ordinary,
safe finding) free of any security gate, matching Protocol 5's precedent that a same-repo log
append is not a cross-repo write.

## CSV Schema

`references/agentteams-remediation-log.csv` — columns, in order:

| Column | Meaning |
|---|---|
| `date` | ISO date the item was logged |
| `source_repo` | Name of the project that surfaced the item |
| `category` | Always `agentteams-remediation` (the log's sole purpose) |
| `summary` | One-sentence statement of the gap |
| `proposed_touch_points` | Candidate file(s)/module(s) in the agentteams tool a fix would touch |
| `status` | Lifecycle state — see below |

The generated agent only ever **appends** rows with `status=open`. It never edits an existing row.

## Status Lifecycle (maintainer-owned)

`open` → `triaged` → `shipped` **or** `wontfix`. Status transitions happen when an agentteams
maintainer reviews the log across projects (mirroring how `agentteams/advisory.py` aggregates
per-repo detector output into one PR-ready report) — not automatically, and not by the generated
agent that logged the row.

## Destination Rule

**Ordinary projects:** append to `references/agentteams-remediation-log.csv` under this project's
own agent-file output directory (the same `<output_dir>/references/` base every other liaison CSV
uses — created via the standard CSV-stub mechanism on `--init`/`--update`). This is expected to be
git-tracked, the same as this project's other agent governance logs.

**Self-referential exception — when this project *is* the AgentTeamsModule repository itself:**
append to the repository's **top-level** `references/agentteams-remediation-log.csv` instead
(alongside its other hand-maintained meta-docs, e.g. `systematic-update-lessons.md`,
`adjacent-repos.md`) — **not** the generic `<output_dir>/references/` path. Reason: AgentTeamsModule
has **two** dogfood output trees, and both are **locally-regenerable build artifacts** rather than
authored deliverables. `.github/agents/` is additionally gitignored; `.claude/agents/` *is*
git-tracked, but only because Claude Code needs it resolvable on disk — tracking it does not make
it authored. Either way a row appended there is overwritten by the next regeneration, which is the
property that matters. Do not read the gitignore status as the reason: it is true of one tree only,
and the exception holds for both. Appending to the generic path would write into a file that either
is untracked or will be regenerated over, and would defeat the entire purpose of this log
(surviving past the session). Do not "fix" this exception by routing it
through the generic path — that would re-introduce the exact bug it exists to avoid.

## Failure Modes To Avoid

| Failure | Prevention |
|---|---|
| Backlog spam from over-eager enumeration | Category definitions require *generalizable* + *novel*; `@adversarial` challenges both before anything is logged; empty lists are the expected common case |
| Silent, soft, easily-skipped step (the original work-summarizer-trigger failure mode) | The subroutine is a named, numbered step inside Workflows 1/2/3, not a buried closeout footnote, and carries an explicit ad-hoc reachability clause |
| CSV/formula injection or secret leakage into a tracked file | Content-safety rule; escalate to `@security` only for that case |
| Duplicate rows for the same underlying gap | Dedup rule, checked twice (subroutine + Protocol 5) |
| Self-referential seed data landing in a regenerable dogfood tree, silently "lost" | Destination Rule's explicit exception; do not route the self-referential case through the generic mechanism, and do not narrow the exception to the gitignored tree — it applies to every regenerable output tree |
| Treating this as a second `@security`-gated cross-repo write | It is a local, same-repo append — Protocol 5 cites Protocol 3 as precedent |

## Related References

- `references/adjacent-repos.md`, `references/adjacent-repos-changelog.csv` — the sibling
  cross-repository logs this pattern is modeled on.
- `@repo-liaison` — the agent that owns Protocol 5 (writes this log).
- `@agent-updater` — applies list (a) repository-infrastructure lessons directly; they are not
  logged here.
<!-- AGENTTEAMS:END content -->
