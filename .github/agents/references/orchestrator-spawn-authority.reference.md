# Orchestrator Spawn-Authority & Query Funnel Reference — LearnPythonStatsEcon

<!--
SECTION MANIFEST — orchestrator-spawn-authority.reference.template.md
| section_id                | designation |
|---------------------------|-------------|
| spawn_authority_reference | FENCED      |
-->

<!-- AGENTTEAMS:BEGIN spawn_authority_reference v=1 -->
## Purpose

Full semantics for **spawner-authority** and the **query funnel** (`@orchestrator` Workflow 12, and
the in-repo child-orchestrator spawn in Workflow 13; `@repo-liaison` Protocol 3's delegate branch).
The orchestrator's rule/workflow text stays terse and **points here** for the operative detail
(living-document policy — one fact in one place).

## The principle: authority follows the spawner

An orchestrator that spins up a neighboring conversation holds authority over it — **regardless of
which repository is "primary."** Whoever spawns a conversation is that conversation's **prime**; the
spawned conversation is its **delegate**.

- A delegate does **not** query the user directly. Its user-facing questions route **up** to its
  prime (subject to the sovereignty carve-out below).
- The prime **resolves first** — investigates code/brief/context and decides — and escalates to the
  user only genuine user-judgment items, consolidated, not piecemeal.
- In a **non-interactive / automated-CLI run** there is no user to ask: the prime resolves all
  inquiries itself and never blocks on a human.
- Every ambiguous decision the prime resolves on the user's behalf is **logged** (see Ledger) for
  post-implementation review.
- **Ambiguous hierarchies are permitted and user-managed** — e.g. a non-primary repo's orchestrator
  managing a management-at-scale repo's orchestrator. The tool does not forbid it; the user owns
  the call.

A **standalone orchestrator with no prime is its own prime** and behaves exactly as it does today.
This is the base case — the funnel never strands it (there is always someone to "route up" to: the
user, directly, when the orchestrator is itself the top of the chain).

## Four authority axes (do not conflate)

Spawner-authority is **not orthogonal** to the project's existing authority model; the axes
**intersect**, and the carve-out + refusal branch below are the reconciliation.

| Axis | Governs | Source |
|---|---|---|
| **Spawner-authority** (this reference) | conversation/query hierarchy — who a spawned conversation reports to and funnels up to | this reference + Workflows 12/13 |
| **Registry-primary** | fleet file-update propagation — which repo is the canonical template source | `references/adjacent-repos.md`, orchestrator Rule 11 |
| **Peer-sovereignty** | constitutional changes to another repo | repo-liaison Invariant Core |
| **Management-authority** | whether a managed repo honours a manager's *signed* directive as authenticated operator direction for the exact non-destructive task it names (so its agents do not re-ask the operator) | C-4's bounded exception in `references/instruction-authority.reference.md` (Management-authority), `references/authorized-managers.txt`, `references/management-directives.log.csv` |

Registry-primary does **not** decide conversation authority; peer-sovereignty is never overridden by
spawner-authority. **Management-authority never overrides peer-sovereignty, C-2, or C-5:** a signed
management directive relays the operator's task assignment, not a licence to destroy, to bypass a
HALT, or to change another repo's constitution — it is auto-refused on any such scope, and the
refusal branch below still applies. The reason the refusal survives even an *authenticated* directive
is that a management directive is **strictly weaker than a live Tier-2 operator instruction**, and
even a genuine Tier-2 instruction may not compel an agent to act outside its own capability grant
(C-3) or Invariant Core; the weaker artifact certainly cannot.

## Reconciliation — two mandatory mechanisms

### Carve-out (for questions)
The prime self-resolves only questions that are **its own** to decide (task allocation,
prioritization, disambiguating the original task list). Any question whose resolution would **bind a
delegate repo's own constitution or user** routes as a **Protocol 3 peer coordination request** —
never silent self-resolution.

### Refusal (for directives)
A prime *directive* (not a question) that a delegate's **own Invariant Core / registry-primary
forbids** must be **refused and reported by the delegate as a peer conflict**. Spawner-authority
never overrides a delegate's sovereignty; the delegate has a refusal path, not only an
escalate-question path. (Without this, the funnel would permit a constitutional inversion.)

## What the runtime enforces vs. what is governance prose (be honest)

- **Enforced (Claude only):** a subagent's output returns to its **spawner**, not the user — so a
  delegate **cannot directly prompt the user**. This is the one hard, runtime-backed guarantee.
- **Governance prose (all frameworks):** *resolve-first*, the *carve-out*, the *refusal branch*, and
  *writing the ledger* are obligations the runtime does not enforce. On Goose/codex/agents-md even
  the "no direct user contact" part is prose. The **escalation report is the only detection
  surface.** Extending the "no direct user contact" guarantee to Goose/copilot-cli via a sandboxed
  subprocess is a separate, security-gated effort (`references/plans/spawn-contained-subordinate.plan.md`).

## In-repo nested orchestrators (Workflow 13)

Spinning up a within-repository conversation for a self-contained **coordinating sub-body-of-work**
creates a **child orchestrator** — spawned via the `agent` tool with a scoping prompt (the sub-goal
plus the child's permitted sub-roster). **Not every subagent becomes an orchestrator** — only a
delegated *coordinating* body of work does. The runtime ensures the child cannot prompt the user
directly (its output returns to the parent); resolve-first remains the parent's governance duty.

### Depth budget (external host fact — tracked via `framework_research`, not repo-verified)
Claude Code caps subagent nesting (default ~3 layers; `CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`) and
withholds the spawn tool at the cap. Arithmetic: top session = depth 0; a child orchestrator =
depth 1; the child's own team = depth 2; anything they try to spawn = depth 3 → withheld. **A nested
orchestrator therefore gets one flat team layer beneath it, and that team cannot sub-delegate.**
Design within this budget; when the cap is reached, flatten remaining work rather than recursing.

### Per-framework reach
- **Claude:** live nested to the depth cap (one team layer beneath a child); funnel's "no direct
  user contact" is runtime-real.
- **copilot-vscode / copilot-cli:** representable via roster/routing; not runtime-contained.
- **codex / agents-md:** documented routing prose only.
- **Goose:** delegation is platform-capped at ONE layer; a child that is itself an orchestrator
  degrades to inlined `summon load()` references — does not run live.

## Escalation ledger + post-implementation report

Ambiguous decisions the prime resolves on the user's behalf append one row to
`references/orchestrator-escalation.log.csv`:

`date,prime,delegate,delegate_repo,query,resolution_mode,decision,ambiguity,needs_user_review,notes`

- `resolution_mode` ∈ `self-resolved | user-forwarded`.
- At session close, the prime emits a **post-implementation review report** listing every
  `needs_user_review=yes` row so the user can review after the fact.
- Writing the ledger is a **governance obligation**, not runtime-enforced — it is the sole detection
  surface for silent self-resolution, so treat it as a closeout gate, not an optional nicety.

## Cross-repo transport (honest limitation)

There is **no automated cross-repo conversation-spawning substrate** today. Cross-repo delegation
rides `@repo-liaison` **Protocol 3's manual/user-transported** Coordination Request, or the host's
cross-session messaging where the operator has enabled it (documented, not emitted by this tool).
<!-- AGENTTEAMS:END spawn_authority_reference -->
