<!-- AGENTTEAMS:BEGIN content v=1 -->
# Code Hygiene Rules — Enforcement Catalog (LearnPythonStatsEcon)

> **Authoritative source for:** `@code-hygiene` agent rule enforcement
> **Agent doc:** `.github/agents/code-hygiene.agent.md`
> **Updated by:** `@agent-updater` after any rule change

---

## Invariant Rules (CH-01 through CH-20)

### CH-01 — No Backup Files in Source Tree

**Enforcement check:**
```
find Textbook/ -name "*.backup" -o -name "*.bak" -o -name "*_old.*" \
  -o -name "*_v[0-9]*.*" -o -name "*_WRONG*" -o -name "*_legacy*" | grep -v node_modules
```
Expected: **zero files**.

### CH-02 — Script Lifecycle: Create → Tag → Execute → Archive/Delete

All one-time scripts must include a purpose header and lifecycle tag. Scripts that have completed their purpose must be deleted.

**Required header for new scripts:**
```
Purpose: <one-line description>
Lifecycle: ONE-TIME | RECURRING | UTILITY
Created: YYYY-MM-DD
```

### CH-03 — No Ad-Hoc Scripts in `Textbook/`

Source directories contain only production code. Investigative, debug, fix, and benchmark scripts must not reside in `Textbook/`.

### CH-04 — Debug Artifacts Must Be Gitignored

Debugging outputs (screenshots, logs, temp data dumps) must be listed in `.gitignore` and never committed.

### CH-05 — Single Source of Truth for Mappings (**Critical**)

Every data mapping, configuration table, or constant set must have exactly one authoritative source. Duplicated mappings across files are a Critical violation.

### CH-06 — Terminal Commands ≤5 Lines; No Inline Heredocs

Any multi-line command exceeding 5 lines must be saved to a script file first. No inline heredocs in agent instructions.

### CH-07 — Standard Module/Component Structure

Project modules must follow a consistent structural pattern. If a standard exists (e.g., `index.js` + `types.ts` per module, or `collector.py` + `uploader.py` per component), deviations are flagged.

### CH-08 — Common Utilities Over Inline Duplication

If logic is duplicated in 3+ locations, it must be extracted to a shared utility. Extraction threshold: **3 occurrences**.

### CH-09 — Config Values in Config Files, Not Code

Environment-specific values (URLs, credentials, thresholds, feature flags) must live in configuration files, environment variables, or constants modules — never hardcoded in business logic.

### CH-10 — Dead Code Removal

Commented-out code blocks, unreachable branches, and unused imports must be removed. Version control preserves history — source files do not.

### CH-11 — Test Files in Dedicated Directory, Not Alongside Source

Test files belong in a dedicated test directory (e.g., `tests/`, `__tests__/`, `spec/`), not mixed with production source files.

### CH-12 — Purposeful Package Init Files

Package init files (`__init__.py`, `index.js`, `mod.rs`) must either re-export public API or be empty. They must not contain business logic.

### CH-13 — No Circular Imports/Dependencies

Module dependency graphs must be acyclic. Circular imports indicate a structural design flaw.

### CH-14 — Docs Reference Code, Don't Duplicate It

Agent files and documentation must reference source files with `#file:` links. They must not duplicate code, data, or configuration inline (>10 lines of data triggers extraction to a reference file).

### CH-15 — No `oldScripts/`/`legacy/` Dirs in Source

Archival directories are not permitted in the source tree. Retired code lives in version control history.

### CH-16 — Temp Files Cleaned After Use

Investigation outputs, temporary data files, and scratch work must be cleaned up before the session closes.

### CH-17 — Import/Require Grouping and Ordering

Imports must follow a consistent grouping convention: stdlib → third-party → local. Within each group, alphabetical ordering is preferred.

### CH-18 — Version-Numbered Files Are Branches, Not Copies

Files like `script_v2.py` or `page_0.1.1.html` indicate copy-paste versioning. Each version should be a branch or tagged commit, not a separate file in the source tree.

### CH-19 — Screenshot/Image Retention Policy

Screenshots and generated images older than 30 days that are not referenced by documentation or test fixtures must be removed.

### CH-20 — Agent Docs Must Not Contradict Each Other (**Critical**)

No two agent files may make contradictory claims about the same fact (e.g., which agent owns a scope, what a priority level is, what a file path resolves to). Contradictions are routed to `@conflict-auditor`.

---

## Extension Rules (CH-21+)

> Add project-specific hygiene rules below using the same ID/Name/Category/Severity structure.

### CH-21 — Validate New Features Before Mainline Integration

**Category:** Testing
**Severity:** High

Newly developed features must be tested or otherwise validated before they are merged into the main program path.

### CH-22 — Type Check Function/Class Inputs

**Category:** Type Safety
**Severity:** High

All function and class inputs must be type-checked (statically, at runtime, or both) to ensure only valid and meaningful input types are accepted.

### CH-23 — Fail Fast on Invalid Inputs

**Category:** Defensive Programming
**Severity:** Critical

Invalid inputs must raise explicit errors. Invalid data must never pass silently, and implicit fallback behavior that masks bad inputs is prohibited.

### CH-24 — Exception Handling Is a Last Resort; Encode Conditions Explicitly

**Category:** Defensive Programming
**Severity:** Critical

`try`/`except`/`finally` is the *last* resort, not the first. Broad or speculative exception handling hides the moment a program breaks, which delays the iterative debug-and-test cycle that depends on knowing immediately that something is wrong.

**Preferred order of control flow:**

1. **Encode expected conditions in data.** Map valid cases in a dictionary / lookup table / dispatch map. Membership and key lookups make the set of handled cases explicit and reviewable.
2. **Guard with explicit checks, then fail hard.** Validate up front and `raise` (or assert) on the unexpected — see [[CH-23]]. A loud failure is a working failure: it points straight at the defect.
3. **Use `try`/`except` only for genuinely unavoidable external failures** — I/O, network, subprocess, third-party calls whose failure modes cannot be predicted by inspection.

**Prohibited patterns:**

- Bare `except:` or `except Exception:` that swallows or logs-and-continues, hiding the real failure.
- `try`/`except` used as flow control where a dictionary lookup, membership test, or `if`/`elif` chain would express the condition directly.
- `except` blocks that return a default / fallback value, masking that the program is in a broken state.
- `finally` used to paper over partial failures instead of letting the error propagate.

**Required when `try`/`except` is genuinely warranted:**

- Catch the *narrowest* applicable exception type, never a bare or blanket catch.
- Either re-raise (optionally wrapped with context) or handle the specific, known recoverable case — never silently continue.

**Enforcement check (illustrative):**
```
grep -rn "except:\|except Exception" Textbook/
```
Each hit must be justified as an unavoidable external-failure boundary; otherwise it is a violation. Prefer a dictionary-driven dispatch or an explicit guard that raises.

### CH-25 — Screen AI-Generated Code Against the Bad-Habits Catalog

**Category:** AI-Generated Code
**Severity:** High

Code authored or substantially edited by an AI agent must be screened against
the AI bad-habits catalog before integration into the main program path. The
catalog (`references/ai-bad-habits-watch.reference.md`, entries `BH-01..BH-NN`)
is a curated, version-controlled list of **code-quality, correctness, and
process** habits specific to AI agents, each mapped to a corrective pattern
(source of truth: `agentteams/ai_bad_habits.py`).

**Security-class AI habits are out of scope here.** Insecure-by-default code
(injection, secrets exposure, excessive agency, supply chain, unbounded
consumption) is owned by `@security` (CWE / OWASP LLM & Web taxonomies +
S-rules). The catalog deliberately does not duplicate them; route every security
finding to `@security`.

The catalog is **authoritative** for the habits it lists; where a `BH-` entry
carries a verified cross-link to an existing `CH-` rule, that rule governs the
detail. Where the cross-link is `—`, the catalog entry is itself the rule.

**Enforcement check (illustrative):**
```
# A new/changed file authored by an agent must not introduce any BH-NN
# code-quality/correctness/process habit whose corrective pattern is unmet.
# Security-class concerns are escalated to @security, not catalogued here.
```

This rule does not duplicate `@security`'s domain (single-source-of-truth,
[[CH-05]] / [[CH-14]]).

### CH-26 — Agent Tool Declarations Must Follow the Principle of Least Authority

**Category:** Agent Governance
**Severity:** High

Each agent's `tools:` YAML field must list only those tools minimally required
to perform the agent's declared function. Excessive grants are a violation even
if the agent never exercises the extra capability in practice.

**Guidance by role archetype:**

| Archetype | Typical tools | Notes |
|---|---|---|
| Auditors, validators, navigators, critics | `read`, `search` | Read-only by nature; no write or execute grants |
| Log-writing agents (conflict log, delivery receipt) | `read`, `edit`, `search` | `edit` scoped to log file writes |
| Execution agents (git, build, format conversion) | `read`, `execute`, `search` | `execute` only when body prose documents a specific shell-invocation step |
| Writing/production agents | `read`, `edit`, `search` | Standard content-creation set |
| Delegation agents (orchestrators, experts) | `read`, `edit`, `search`, `execute`, `agent` | Only when all are justified by declared procedures |

**Prohibited patterns:**
- `execute` on an agent whose Invariant Core and declared procedures contain no shell command invocation
- `--allow-all-tools` on any subprocess invocation of a Copilot/AI CLI (use `--available-tools=<list>` instead)
- Tool grants copied from a similar agent without re-evaluating the target agent's actual needs
- Granting `agent` to an agent that has no `handoffs:` entries and no sub-agent delegation procedures

**Enforcement check:**
```
# For each .agent.md file: read its tools: list and its Invariant Core / procedures.
# Flag any tool that has no corresponding step or body reference justifying its use.
# Verify no subprocess call uses --allow-all-tools.
grep -rn "\-\-allow-all-tools" Textbook/
```

### CH-27 — Prefer Long-Lived Utilities Over Ad-Hoc Scripts

**Category:** Modularity / Reuse
**Severity:** Medium

*Applies to code artifacts.* If a feature being created or managed is **likely to
be used again**, the logic that creates or manipulates it must live in a
long-lived, reusable utility (module, library function, CLI subcommand) — not in
an ad-hoc script, **and not in a script merely *tagged* `RECURRING`/`UTILITY` yet
re-authored each time.**

**Distinct violation (not redundant with [[CH-02]]/[[CH-03]]):** CH-02 requires
*tagging and deleting* one-off scripts and CH-03 keeps ad-hoc scripts out of
source — both are satisfied by an agent that nonetheless keeps writing fresh
throwaway scripts for recurring work. CH-27 adds the affirmative duty those rules
do not state: recurring operational work must be **promoted to a durable utility**,
not repeatedly re-scripted.

**Boundary vs. [[CH-08]] (rule of three) and BH-03:** CH-27 does **not** lower
CH-08's 3-occurrence extraction threshold and does **not** mandate premature
abstraction of genuinely single-use helpers (BH-03 in the bad-habits catalog). The
trigger is foreseeable recurrence judged from the task, not raw repetition count.

**Report-only.** Like every `@code-hygiene` finding, CH-27 is reported; it triggers
no `@cleanup` deletion of its own.

**Enforcement check (illustrative):**
```
# Flag repeated/dated one-off scripts doing equivalent work (fix_*, run_*_v2,
# dated throwaways), or scripts tagged RECURRING/UTILITY that duplicate logic
# better housed in a module. Recommend promotion to a long-lived utility.
```

### CH-28 — Prefer Minimal, Scoped Edits

**Category:** Change Discipline
**Severity:** Medium (advisory)

*Applies to code artifacts.*

> **Constraints first (closes the "minimal-diff" loophole):** CH-28 NEVER excuses
> skipping a *required* change. Dead-code removal ([[CH-10]]), correctness guards
> ([[CH-23]]/[[CH-24]]), and type checks ([[CH-22]]) are mandatory **even when they
> add lines.** CH-28 does NOT block *sanctioned, scoped* refactors ([[CH-07]]
> structure carves, [[CH-08]] extractions) or `@agent-refactor`'s mandate — those
> are intentional work. CH-28 targets only **incidental** scope creep within an
> otherwise-unrelated change.

Subject to the constraints above: a change should touch only the lines its task
requires. When an outcome is achievable in a small, localized diff, do not rewrite
surrounding code, reformat untouched regions, or expand scope. Gratuitous churn
obscures intent, inflates review cost, and is a common AI-agent failure mode (see
BH-10 in the bad-habits catalog).

**Advisory & precedented.** CH-28 is reported, never blocking, and triggers no
deletion. It is not mechanically counted — its enforcement check is illustrative
**exactly as [[CH-24]] and [[CH-25]] already are.**

**Enforcement check (illustrative):**
```
# Judgment-based: report a diff whose churn (rewrites, reformatting of untouched
# regions, scope expansion) appears disproportionate to the stated task. Never
# flag a required change (CH-10/CH-22/CH-23/CH-24) or a sanctioned CH-07/CH-08
# refactor. No automated metric.
```

<!-- Example:
### CH-21 — Project-Specific Rule Name

**Category:** <category>
**Severity:** <severity>

Description and enforcement check.
-->
<!-- AGENTTEAMS:END content -->
