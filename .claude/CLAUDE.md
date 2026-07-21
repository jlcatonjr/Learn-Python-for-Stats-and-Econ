<!--
SECTION MANIFEST — copilot-instructions.template.md
| section_id            | designation   | notes                                    |
|-----------------------|---------------|------------------------------------------|
| project_overview      | FENCED        | Name, goal, deliverable type, output fmt |
| directory_structure   | FENCED        | Path/purpose table                       |
| output_conventions    | FENCED        | Authoring and build conventions          |
| agent_team            | FENCED        | Full agent team list                     |
| authority_hierarchy   | FENCED        | Source hierarchy list                    |
| source_repositories   | FENCED        | Authority source entries                 |
| constitutional_rules  | USER-EDITABLE | Project may extend or customise          |
| style_rules           | USER-EDITABLE | Project may extend or customise          |
-->

# LearnPythonStatsEcon — Copilot Instructions

> This file defines the conventions, authority hierarchy, and agent team structure for all GitHub Copilot agents in LearnPythonStatsEcon.

---

<!-- AGENTTEAMS:BEGIN project_overview v=1 -->
## Project Overview

**Name:** LearnPythonStatsEcon
**Goal:** Author and maintain a Python programming textbook for economists and social scientists, covering core Python, statistical analysis, econometrics, and data visualization. The textbook is delivered as a series of Jupyter notebooks organized into chapters, with accompanying tutorials, in-class demonstrations, and student projects.
**Deliverable type:** Jupyter notebooks, tutorial notebooks, in-class demonstration notebooks and student project notebooks
**Output format:** Jupyter notebooks (.ipynb)
<!-- AGENTTEAMS:END project_overview -->

---

<!-- AGENTTEAMS:BEGIN directory_structure v=1 -->
## Directory Structure

| Path | Purpose |
|------|---------|
| `Textbook/` | Primary authored deliverables |
| `build/` | Compiled/converted output artifacts |
| `figures/` | Diagrams and figures |
| `N/A - no citation database configured for this project` | Reference/bibliography database |
| `.github/agents/` | Agent definition files |
| `.github/agents/references/` | Shared reference data |
<!-- AGENTTEAMS:END directory_structure -->

---

<!-- AGENTTEAMS:BEGIN output_conventions v=1 -->
## Output Conventions

- All primary deliverables are authored in `Textbook/` as `Jupyter notebooks, tutorial notebooks, in-class demonstration notebooks and student project notebooks`
- Compiled output lives in `build/` and is **never edited directly**
- Figures are generated from source files in `figures/` — source files are authoritative
- Every deliverable must correspond to a Component Spec defined by a workstream expert
- Work summaries are authored in `workSummaries/` from canonical `tmp/by-week/` plan artifacts, legacy `tmp/` fallbacks, and git history
<!-- AGENTTEAMS:END output_conventions -->

---

<!-- AGENTTEAMS:BEGIN agent_team v=1 -->
## Agent Team

### Orchestrator
- `@orchestrator` — coordinates all agents; entry point for all user requests

### Governance Agents
- `@navigator` — project structure and file location
- `@security` — destructive operation clearance
- `@code-hygiene` — architecture enforcement and anti-sprawl auditor
- `@adversarial` — presupposition critic
- `@conflict-auditor` — consistency enforcement
- `@conflict-resolution` — ACCEPT/REJECT/REVISE decisions on flagged conflicts
- `@cleanup` — artifact removal
- `@agent-updater` — documentation synchronization
- `@agent-refactor` — spec compliance and reference extraction
- `@repo-liaison` — cross-repository impact tracking and coordination
- `@git-operations` — git/github operations and merge strategy workflow

### Domain Agents
- `@work-summarizer` — synthesizes daily/weekly/monthly work summaries from plan artifacts and git history
- `@primary-producer` — drafts and revises primary deliverables
- `@quality-auditor` — read-only structural and prose quality audit
- `@cohesion-repairer` — repairs within-section cohesion failures
- `@style-guardian` — enforces voice and style fidelity
- `@technical-validator` — verifies technical accuracy against authority sources
- `@output-compiler` — assembles components into the final deliverable package
- `@visual-designer` — creates and revises diagrams and figures
- `@tool-doc-researcher` — specialized domain agent

### Workstream Experts
- `@ch1-essentials-expert` — Chapter 1 — The Essentials
- `@ch2-lists-expert` — Chapter 2 — Working With Lists
- `@ch3-numpy-pandas-expert` — Chapter 3 — NumPy, Pandas, and Matplotlib
- `@ch4-functional-expert` — Chapter 4 — Functional Programming and Rudimentary Statistics
- `@ch5-probability-expert` — Chapter 5 — Probability Distributions
- `@ch6-hypothesis-expert` — Chapter 6 — Hypothesis Testing
- `@ch7-ols-expert` — Chapter 7 — Building an OLS Regression Model
- `@ch8-advanced-expert` — Chapter 8 — Advanced Data Analysis
- `@ch9-abm-expert` — Chapter 9 — Agent-Based Modeling
<!-- AGENTTEAMS:END agent_team -->

---

<!-- AGENTTEAMS:BEGIN tone_and_style v=1 -->
## Tone and Style

Default to terse output for read-only auditor and governance roles
(`@security`, `@adversarial`, `@code-hygiene`, `@conflict-auditor`,
`@navigator`, `@quality-auditor`, `@technical-validator`,
`@post-production-auditor`, `@module-doc-validator`,
`@reference-manager` in read mode): respond in ≤200 words unless
the task requires longer output. Producing roles
(`@primary-producer`, `@module-doc-author`, `@content-enricher`,
`@output-compiler`, `@orchestrator` when summarizing a multi-step
session) emit the deliverable in full and are exempt from this
default.

Terse mode reduces consumer-harness token consumption on the
common case of audit-and-route turns. Producing roles override the
default explicitly by saying so in their first line.
<!-- AGENTTEAMS:END tone_and_style -->

<!-- AGENTTEAMS:BEGIN authority_hierarchy v=1 -->
## Authority Hierarchy

1. **Textbook/Chapter 1 - The Essentials.ipynb** (`Textbook/Chapter 1 - The Essentials.ipynb`) — general
2. **Textbook/Chapter 7 - Building an OLS Regression Model.ipynb** (`Textbook/Chapter 7 - Building an OLS Regression Model.ipynb`) — general
3. **ECON 411 611 Syllabus.docx** (`ECON 411 611 Syllabus.docx`) — general
<!-- AGENTTEAMS:END authority_hierarchy -->

---

## Constitutional Rules

1. **Security first** — destructive operations require `@security` clearance
2. **Code hygiene second** — code changes require `@code-hygiene` audit before merge
3. **Authority hierarchy is ground truth** — no agent may contradict a higher-authority source
4. **Primary deliverables are the canonical output** — build artifacts are derived, never primary
5. **No fabricated references** — every citation must be verifiable in `N/A - no citation database configured for this project`
6. **Voice fidelity** — style governance rulings are authoritative when a style-governance agent is present
7. **Living documentation** — agent docs must not accumulate stale content
8. **Always close with `@conflict-auditor`** — required after any multi-file change session
9. **Every request must generate a plan** — any request involving two or more implementation steps (steps that write, create, rename, delete, or make agent decisions) must produce: (a) a summary saved to `tmp/by-week/YYYY-Www/<plan-slug>.plan.md` and (b) a step-by-step CSV saved to `tmp/by-week/YYYY-Www/<plan-slug>.steps.csv` before the first step executes; the CSV must include columns: `step`, `agent`, `action`, `inputs`, `outputs`, `status`, `notes` (and may include an optional `depends_on` column listing the `step` ids a row depends on, enabling parallelization analysis); initial `status` for all rows is `pending`; after each step completes, pass remaining steps through `@adversarial` and `@conflict-auditor` before proceeding; create the week folder if it does not exist and read legacy undated plans from `tmp/` when canonical week-organized storage is absent
10. **Completed plans must be captured in daily work summaries** — when a plan reaches all `done` during a session, invoke `@work-summarizer` to append/update `workSummaries/daily/YYYY-MM-DD.md` before closeout

---

<!-- AGENTTEAMS:BEGIN source_repositories v=1 -->
## Source Repositories

- `Textbook/Chapter 1 - The Essentials.ipynb` — general
- `Textbook/Chapter 7 - Building an OLS Regression Model.ipynb` — general
- `ECON 411 611 Syllabus.docx` — general
<!-- AGENTTEAMS:END source_repositories -->

---

## Style Rules

No project-specific style rules defined.
