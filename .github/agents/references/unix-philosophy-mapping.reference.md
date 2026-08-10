<!-- AGENTTEAMS:BEGIN content v=1 -->
# Unix Philosophy — Code Hygiene Mapping (LearnPythonStatsEcon)

> **Purpose:** Document how code-hygiene rules align with principles from Unix system design and software architecture
> **Applies to:** CH-01 through CH-29 rule interpretations
> **Relationship:** This is a *reference for reasoning*, not the authoritative source of rules. See `code-hygiene-rules.reference.md` for the complete enforcement catalog.
> **Authority Position:** Complements (not supersedes) the authority hierarchy defined in orchestrator.agent.md
> **Maintenance:** Updated by `@agent-updater` when code-hygiene-rules.reference.md changes AND when interpretations of Unix principles need clarification
> **Source Attribution:** This mapping draws from Doug McIlroy's foundational work, Eric Raymond's "The Art of UNIX Programming", and domain expertise in modular software architecture. It represents one interpretation among several scholarly framings of Unix thought.

---

## Overview

The Unix philosophy emerged from decades of systems engineering (circa 1970s–1980s) and established principles that remain relevant to modular software design. Many code-hygiene rules, when compared against these principles, show strong alignment—either by deliberate design or by convergence on proven patterns.

This mapping serves as a **reasoning reference**: it explains *why* certain hygiene rules exist, grounds them in established design wisdom, and helps guide extensions to the rule set.

### Five Core Principles (Douglas McIlroy et al.)

These principles are drawn from Unix system design literature and represent a widely-recognized framing of Unix philosophy. This reference uses these five as an organizational framework.

| Principle | Essence | Implication |
|-----------|---------|------------|
| **Do One Thing, Do It Well** | Each component has a single, well-defined responsibility | CH-03, CH-07, CH-08, CH-12 |
| **Make Programs That Work Together** | Components must be composable via clean, minimal interfaces | CH-05, CH-13, CH-14, CH-17 |
| **Design for Simplicity** | Prefer simple, obvious designs over clever, complex ones | CH-06, CH-09, CH-10 |
| **Embrace Modularity** | Small, independent modules reduce coupling and complexity | CH-01, CH-02, CH-04, CH-15, CH-16 |
| **Value Transparency and Clarity** | Code and behavior must be discoverable and understood without mystery | CH-11, CH-18, CH-19, CH-20 |

---

## Rule-to-Principle Mapping

> **Important:** This mapping is organized by principle strength. **Tier 1 rules** show strong Unix alignment. **Tier 2 rules** are pragmatic project requirements that happen to align. **Tier 3 rules** are project-specific and may not reflect Unix philosophy directly, but serve operational needs.

### 1. Do One Thing, Do It Well

This principle advocates for **focused, single-purpose components** that excel at their designated task without scope creep. It appears in McIlroy's foundational Unix philosophy statement: "Write programs that do one thing and do it well."

**Alignment with Rules:**

| Rule | Tier | Connection |
|------|------|-----------|
| **CH-03** — No Ad-Hoc Scripts in `Textbook/` | 2 | Source code contains only intentional, production-focused logic. Project-specific need for clean source boundaries. |
| **CH-07** — Standard Module/Component Structure | 1 | Enforces consistent structure within each module. Each module has one clear purpose (e.g., `collector.py` does collection; `uploader.py` does uploading). |
| **CH-08** — Common Utilities Over Inline Duplication | 1 | Extraction of repeated logic into shared utilities ensures each utility has one, clear responsibility. |
| **CH-12** — Purposeful Package Init Files | 1 | Package init files must either re-export public API or be empty—no business logic. A single, clear purpose. |

---

### 2. Make Programs That Work Together

This principle requires **clean interfaces and interoperability**. McIlroy stated: "Write programs to work together." Programs should compose easily without hidden dependencies or state sharing.

**Alignment with Rules:**

| Rule | Tier | Connection |
|------|------|-----------|
| **CH-05** — Single Source of Truth for Mappings (**Critical**) | 1 | Composable programs depend on a single, authoritative source for shared data. Multiple conflicting sources break interoperability. |
| **CH-13** — No Circular Imports/Dependencies | 1 | Acyclic dependency graphs enable components to be reused, tested, and understood in isolation. Circular dependencies destroy composability. |
| **CH-14** — Docs Reference Code, Don't Duplicate It | 1 | Documentation that references (not duplicates) code ensures the doc and code stay in sync. Users trust a single, authoritative source. |
| **CH-17** — Import/Require Grouping and Ordering | 2 | Standardized import ordering makes dependency chains obvious at a glance. Project-specific practice. |

---

### 3. Design for Simplicity

This principle rejects unnecessary complexity. **Simple designs are easier to understand, test, and modify.** While Unix philosophy emphasizes simplicity in a systems context, this principle applies broadly to code design.

**Alignment with Rules:**

| Rule | Tier | Connection |
|------|------|-----------|
| **CH-06** — Terminal Commands ≤5 Lines; No Inline Heredocs | 2 | Keeps command logic readable and maintainable. Multi-line commands belong in scripts, not inline. Project-specific practice. |
| **CH-09** — Config Values in Config Files, Not Code | 1 | Separates configuration (values that change) from logic (rules that don't). Simplifies understanding and updating. |
| **CH-10** — Dead Code Removal | 2 | Removes noise and clutter. Dead code increases cognitive load and masks true intent. Project-specific practice. |

---

### 4. Embrace Modularity

This principle structures systems as **independent, cooperating modules**. Each module is a unit of development, testing, and deployment. Modularity is a core concept in Unix philosophy and broader software architecture.

**Alignment with Rules:**

| Rule | Tier | Connection |
|------|------|-----------|
| **CH-01** — No Backup Files in Source Tree | 2 | Eliminates clutter that obscures module boundaries and ownership. Project-specific housekeeping. |
| **CH-02** — Script Lifecycle: Tag → Execute → Delete | 2 | Ensures scripts are temporary and cleaned up. Prevents accidental "proto-modules" that muddy the codebase. Project-specific practice. |
| **CH-04** — Debug Artifacts Must Be Gitignored | 2 | Debug outputs pollute the module manifest. Gitignoring keeps module definition clean. Project-specific practice. |
| **CH-15** — No `oldScripts/`/`legacy/` Dirs in Source | 2 | Prevents dead-code directories that complicate module structure. Version control preserves history. Project-specific rule. |
| **CH-16** — Temp Files Cleaned After Use | 2 | Investigative output must not leak into the module's final state. Project-specific practice. |

---

### 5. Value Transparency and Clarity

This principle insists on **discoverability and explicitness**. Hidden behaviors, undocumented assumptions, and magic all violate this principle. Unix philosophy emphasizes "transparency" through simple text formats and predictable behavior.

**Alignment with Rules:**

| Rule | Tier | Connection |
|------|------|-----------|
| **CH-11** — Test Files in Dedicated Directory, Not Alongside Source | 1 | Test organization makes test scope clear and explicit. Tests are not hidden or mixed with business logic. |
| **CH-18** — Version-Numbered Files Are Branches, Not Copies | 2 | Version files in the source tree hide the version-control history that should be the authoritative source. This violates transparency. Project-specific practice. |
| **CH-19** — Screenshot/Image Retention Policy | 3 | Orphaned screenshots obscure which documentation they belong to. Clear retention rules make ownership explicit. Pure project-specific housekeeping; no Unix philosophy connection. |
| **CH-20** — Agent Docs Must Not Contradict Each Other (**Critical**) | 1 | Contradictory claims in documentation hide the true state. Transparency requires a single, consistent narrative. |

---

## Extension Rules (CH-21+) and Design Principles

The repository adds nine enforcement rules (CH-21 through CH-29). CH-21–CH-26 are
largely **project-specific operational requirements** complementary to Unix
philosophy; CH-27, CH-28, and CH-29 align *directly* with it (Software Tools, the
Rule of Simplicity, and Software Tools again, respectively):

| Rule | Tier | Principle Connection |
|------|------|---------------------|
| **CH-21** — Validate New Features Before Mainline Integration | 3 | **Defensive Programming.** Untested features create hidden states and unpredictable behaviors. Validation ensures the feature works before integration. (Project-specific mandate; not Unix-derived.) |
| **CH-22** — Type Check Function/Class Inputs | 3 | **Type Safety.** Type checking makes input contracts explicit. Implicit type coercion hides expectations and causes subtle bugs. (Project-specific mandate; complements simplicity principles.) |
| **CH-23** — Fail Fast on Invalid Inputs | 3 | **Defensive Programming.** Explicit errors reveal problems early. Silent failures hide bugs deep in a system, making them expensive to diagnose. (Project-specific mandate; aligns with transparency but not Unix-specific.) |
| **CH-24** — Exception Handling Is a Last Resort; Encode Conditions Explicitly | 3 | **Transparency + Defensive Programming.** Encoding cases in dictionaries and failing hard keeps the program's true state visible; broad `try`/`except` hides brokenness and defeats fast iterative debugging. Aligns with "Value Transparency and Clarity" — behavior must be discoverable, not buried under blanket error suppression. (Project-specific mandate; reinforces [[CH-23]].) |
| **CH-25** — Screen AI-Generated Code Against the Bad-Habits Catalog | 3 | **Process / Quality.** AI-authored code carries recurring quality/correctness habits; screening catches them before integration. (Project-specific mandate; security-class habits are `@security`'s domain.) |
| **CH-26** — Agent Tool Declarations Follow Least Authority (PoLA) | 2 | **Make Programs That Work Together.** Minimal authority mirrors minimal, well-scoped interfaces — an agent granted only what it needs is easier to reason about and compose. (Governance mandate.) |
| **CH-27** — Prefer Long-Lived Utilities Over Ad-Hoc Scripts | 1 | **Software Tools / "Make each program do one thing well."** Recurring work belongs in durable, reusable tools, not throwaway scripts. Directly expresses the Unix "build reusable tools" ethos. |
| **CH-28** — Prefer Minimal, Scoped Edits | 1 | **Rule of Simplicity / Rule of Economy ("Design for Simplicity").** The smallest change that satisfies the task keeps intent and program state legible; gratuitous churn is the complexity Unix philosophy warns against. (Advisory; never overrides required changes or sanctioned refactors.) |
| **CH-29** — Script-First Output Discipline: Build and Reuse Reference Files | 1 | **Software Tools / "Write programs to work together" via durable reference artifacts.** Choosing a script over manual, one-off work — and capturing what was learned about each language/library in a reusable reference file — is the same "build reusable tools" ethos as [[CH-27]], applied at the moment of output production rather than after recurrence is observed. |

---

## Why This Mapping Matters

Understanding the alignment between rules and design principles helps developers:

1. **Grasp the reasoning** — Rules are not arbitrary constraints but express proven design wisdom
2. **Make consistent tradeoffs** — When pragmatism requires bending a rule, knowing the principle helps evaluate the cost
3. **Extend the rule set** — New rules should be grounded in principles or clearly justified as project-specific
4. **Maintain over time** — Knowing *why* a rule exists makes it easier to keep it in sync as the project evolves

**Caveat:** This mapping documents which rules *happen to align with* Unix principles. It does not claim that Unix philosophy is the only valid source of design wisdom, or that all project rules must derive from it. The code-hygiene agent also enforces project-specific rules (CH-21–CH-26) that serve operational needs independent of Unix philosophy, plus CH-27–CH-28 which align with it directly.

---

## How to Use This Reference

**For `@code-hygiene` agent enforcement:**
- When a rule is violated, consult this mapping to understand which design principle is at stake and why it matters.
- Be aware that Tier 1 rules express foundational principles, while Tier 2–3 rules are pragmatic project needs.

**For rule extensions or modifications:**
- New rules should be clearly classified (Tier 1, 2, or 3) and justified.
- If a rule evolves such that its tier changes (e.g., from Tier 1 to Tier 2), update this mapping and notify `@agent-updater`.

**For maintenance and governance:**
- When `code-hygiene-rules.reference.md` changes, this file must be updated in coordination (see header notes).
- If Unix philosophy interpretations shift or sources update, reflect changes here.

**For developers and new team members:**
- When unsure about code structure, ask: "Which design principle does this serve?" The answer often guides the right approach.
- Understand that not all rules express foundational principles—some are project-specific—so tradeoffs are contextual.

---

## Reference Sources

- **Doug McIlroy** (1978). Bell Labs Unix Philosophy: "Write programs that do one thing and do it well. Write programs to work together."
- **Eric Raymond** (2003). *The Art of UNIX Programming*. Addison-Wesley.
- **Peter Salus** (1994). *A Quarter Century of UNIX*. Addison-Wesley.
- **AgentTeamsModule Architecture** (`build-team-plan.md`): Project-specific operational requirements and constitutional rules.

<!-- AGENTTEAMS:END content -->
