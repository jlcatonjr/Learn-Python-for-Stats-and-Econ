<!-- AGENTTEAMS:BEGIN content v=1 -->
# Parallelization Reference

How this team identifies **independent** plan steps and dispatches them in parallel
**waves** instead of strictly one at a time — under a conservative, fail-safe
heuristic that never weakens the per-step audit. Operative workflow: **Workflow 0A
(Parallelization Analysis)** in the orchestrator.

## The signal: optional `depends_on`

The plan-steps CSV (`tmp/by-week/YYYY-Www/<plan-slug>.steps.csv`) uses the required
columns `step,agent,action,inputs,outputs,status,notes` and may add an **optional
`depends_on`** column: a space- or comma-separated list of the `step` ids a row
depends on. An empty (or absent) `depends_on` means "no declared prerequisite." A
7-column CSV without the column stays valid — every step is then treated
conservatively.

Populate `inputs`/`outputs` with concrete repo-relative paths. Independence is
derived from these **footprints**, not from the prose.

## The analyzer

```
python -m agentteams.parallel_plan tmp/by-week/<week>/<plan>.steps.csv
python -m agentteams.parallel_plan PLAN_A.steps.csv PLAN_B.steps.csv   # cross-plan
python -m agentteams.parallel_plan <plan>.steps.csv --json
```

From Python:

```python
from pathlib import Path
from agentteams.parallel_plan import analyze_plan, render_markdown
print(render_markdown(analyze_plan(Path("tmp/by-week/<week>/<plan>.steps.csv"))))
```

On Claude teams the `parallelize-plan` skill wraps the same call.

## What independence means here (heuristic, not proof)

Two steps may share a wave **only** when **all** hold:

1. **Disjoint writes** — their `outputs` footprints do not overlap (path equality
   or directory/file containment both count as overlap).
2. **No read-after-write** — neither reads (`inputs`) a path the other writes
   (`outputs`). Shared *reads* are fine.
3. **No shared mutable state** — neither touches the denylist: git / the git
   index, databases (`db`, `sql`), locks/lockfiles, the network (`http`, `://`),
   running servers, ports, deployments, or migrations.

Anything else runs sequentially. Failure modes are handled **fail-safe**:

- A step with an **empty/unparseable footprint** is treated as non-independent
  (its own singleton wave).
- An **undeclared read-after-write** is detected from footprints and an implicit
  ordering edge is added, so the schedule stays correct even if `depends_on` was
  under-declared.
- A **dependency cycle** (declared or footprint-implied) is a **blocking error** —
  no schedule is emitted until the CSV is fixed.

## Execution contract (Workflow 0A)

For each wave, in order:

- **Dispatch:** concurrently via the `agent` tool **only where the host runtime
  supports concurrent subagents** (e.g. Claude); otherwise treat the wave as an
  "any-order" set and run its members sequentially.
- **Audit at wave join:** run `@conflict-auditor` on each member's deliverable
  after it completes. Because members are footprint-disjoint, these per-member
  audits commute — this preserves the per-step effect-audit guarantee without
  serializing dispatch. Run `@adversarial` once per wave on the remaining plan.
- **Revise & re-analyze** `status`/`depends_on` on the remaining `pending` steps
  before the next wave.

## Never batched (singleton carve-outs)

Destructive (file deletion, bulk edit ≥3 files), cross-repository, and
`agentteams … --bridge-refresh` steps are **never** placed in a multi-member wave.
Each runs as its own singleton wave and goes through its full per-step clearance
first (`@security`; `@repo-liaison` + `@security`; the
`references/bridge-refresh-safety.md` Pre-Flight) regardless of footprint analysis.

## Cross-plan: any-order, not concurrency

`python -m agentteams.parallel_plan` over several `*.steps.csv` reports which open
plans are mutually **non-blocking** (disjoint footprints — safe to advance in any
order). In a single orchestrator session this is a *scheduling note*, not
simultaneous execution; genuine cross-plan concurrency needs a separate substrate
and is out of scope.
<!-- AGENTTEAMS:END content -->
