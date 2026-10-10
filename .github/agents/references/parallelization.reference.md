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

## Coordinated concurrency for overlapping work

This section **inverts** Workflow 0A's "overlap → serialize" default — but only
inside a narrow, opt-in envelope. Workflow 0A serializes every footprint overlap on
purpose, because an *undeclared* overlap can be a forgotten data dependency and
serializing the ambiguous case is the safe default. Coordinated Concurrency does not
weaken that default. It activates **only** for steps the operator has **explicitly
tagged with a shared `coordinate` group label**; it does not promote an untagged
overlap. For a tagged group whose members must share files, it dispatches concurrent
conversations that each claim **disjoint sub-regions** of the shared file-set so they
coordinate instead of stepping on each other. This **reduces** collision risk; it is
not a lock and does not prevent clobbering — the disjoint-sub-region discipline plus
the serialize fallback are the actual safety.

The mechanism is **framework-neutral**: the coordination ledger (below) is a plain
file that any host reads and appends with the read/edit capabilities every adapter
already declares, so coordination works on any agentic system (Claude, goose,
copilot, codex, agents-md, …). Native inter-agent messaging is an **optional**
enhancement layered on top — **Claude first** (agent-to-agent messaging /
ListAgents + SendMessage), **then goose** — with the ledger as the durable source of
truth. Where a host lacks messaging, the ledger alone coordinates and the feature
still works.

### When NOT to coordinate

Serialize (do not coordinate) whenever any of these hold — this is the discriminator:

- **Untagged footprint overlap.** Overlap without a shared `coordinate` label keeps
  serializing exactly as Workflow 0A does today — this is the fail-safe default.
- **Any shared mutable state** — the denylist (git / git index, databases, locks,
  network, running servers, ports, deployments, migrations).
- **Destructive, cross-repository, or `--bridge-refresh`** steps.
- **A genuine data dependency** — a declared `depends_on` among members → serialize.

A **missing `depends_on` is NOT a coordination signal.** Coordination is strictly
opt-in via the `coordinate` label; the analyzer does not infer coordination from the
absence of a dependency, because a footprint-overlap-without-`depends_on` is the
exact population Workflow 0A's fail-safe serializes on purpose (an under-declared
real dependency looks identical to legitimate co-editing).

### The coordination ledger

The coordination channel is an append-only CSV at
`tmp/by-week/YYYY-Www/<plan-slug>.coord.csv` with columns
`entry,agent,region,action,status,note`:

- `entry` — monotonically increasing integer, one per event.
- `agent` — the agent/conversation appending the row.
- `region` — a repo-relative `path`, or `path#section`, naming the **disjoint
  sub-region** being worked (distinct files, or distinct named sections/functions).
- `action` — one of `claim` | `release` | `update` | `handoff` | `block` | `done`.
- `status` — `open` | `resolved`.
- `note` — short free text.

The ledger is **append-only** — prior rows are immutable (append, do not rewrite). It
**reduces**, does not prevent, same-region clobbering — final safety is the
disjoint-sub-region discipline plus the serialize fallback. It is not a lock.

### Coordination cadence

Each member follows this cadence:

1. **Partition first.** Before dispatch, split the shared file-set into disjoint
   sub-regions and assign one per member; concurrency is safe because members write
   **different** sub-regions.
2. **Read before write.** Re-read the ledger before touching any region, and again at
   each sub-task boundary.
3. **`claim`** your assigned sub-region (append a `claim` row) before writing it.
4. **`release`/`done`** after finishing the sub-region.

Where the host provides native inter-agent messaging (**Claude first, then goose**),
members also message peers directly, but the **ledger remains the durable source of
truth**.

### Resolving contention (not stepping on each other)

If two members claim the **same** region, the **lower `entry` wins** it; the other
**re-scopes to a disjoint sub-region or serializes behind the winner**. Unresolved
contention escalates to `@orchestrator`. This is the mechanism that keeps concurrent
members from stepping on each other: contested regions collapse back to serialized
ordering rather than racing.

### Audit cadence for coordinated groups

Because members write **disjoint sub-regions**, per-member audits largely commute:

- Run `@conflict-auditor` on **each member's output as it completes**.
- Then run **one combined consistency audit over the shared file-set at group join**,
  to catch cross-member interactions.
- Then run `@adversarial` once on the remaining plan.

This is stronger than a single combined audit and preserves Workflow 0A's per-step
effect-audit guarantee.

### Excluded from coordination (carve-outs)

Destructive (file deletion, bulk edit ≥3 files), cross-repository,
`agentteams … --bridge-refresh`, and shared-mutable-state steps are **excluded from**
coordination. They stay singleton and go through their full per-step clearance — the
**same denylist as Workflow 0A** — regardless of any `coordinate` tag.

### The analyzer surface

`coordination_candidates()` keys off the opt-in `coordinate` column only, and the
`--json` output exposes a top-level `coordination_candidates` key. Its groups are
**advisory** candidates: the orchestrator makes the final call and still applies the
singleton carve-outs above. The analyzer does not promote an untagged overlap to a
coordination group, and it flags any tagged group whose members also declare a mutual
`depends_on` (a real dependency → serialize, do not coordinate).
<!-- AGENTTEAMS:END content -->
