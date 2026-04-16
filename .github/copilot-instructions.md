# LearnPythonStatsEcon — Copilot Instructions

> This file defines the conventions, authority hierarchy, and agent team structure for all GitHub Copilot agents in LearnPythonStatsEcon.

---

## Project Overview

**Name:** LearnPythonStatsEcon
**Goal:** Author and maintain a Python programming textbook for economists and social scientists, covering core Python, statistical analysis, econometrics, and data visualization. The textbook is delivered as a series of Jupyter notebooks organized into chapters, with accompanying tutorials, in-class demonstrations, and student projects.
**Deliverable type:** Jupyter notebooks, tutorial notebooks, in-class demonstration notebooks and student project notebooks
**Output format:** Jupyter notebooks (.ipynb)

---

## Directory Structure

| Path | Purpose |
|------|---------|
| `Textbook/` | Primary authored deliverables |
| `build/` | Compiled/converted output artifacts |
| `figures/` | Diagrams and figures |
| `N/A — no citation database configured for this project` | Reference/bibliography database |
| `.github/agents/` | Agent definition files |
| `.github/agents/references/` | Shared reference data |

---

## Output Conventions

- All primary deliverables are authored in `Textbook/` as `Jupyter notebooks, tutorial notebooks, in-class demonstration notebooks and student project notebooks`
- Compiled output lives in `build/` and is **never edited directly**
- Figures are generated from source files in `figures/` — source files are authoritative
- Every deliverable must correspond to a Component Spec defined by a workstream expert

---

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

### Domain Agents
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

---

## Authority Hierarchy

1. **Textbook/Chapter 1 - The Essentials.ipynb** (`Textbook/Chapter 1 - The Essentials.ipynb`) — general
2. **Textbook/Chapter 7 - Building an OLS Regression Model.ipynb** (`Textbook/Chapter 7 - Building an OLS Regression Model.ipynb`) — general
3. **ECON 411 611 Syllabus.docx** (`ECON 411 611 Syllabus.docx`) — general

---

## Constitutional Rules

1. **Security first** — destructive operations require `@security` clearance
2. **Code hygiene second** — code changes require `@code-hygiene` audit before merge
3. **Authority hierarchy is ground truth** — no agent may contradict a higher-authority source
4. **Primary deliverables are the canonical output** — build artifacts are derived, never primary
5. **No fabricated references** — every citation must be verifiable in `N/A — no citation database configured for this project`
6. **Voice fidelity** — `@style-guardian` is the sole arbiter of voice deviation rulings
7. **Living documentation** — agent docs must not accumulate stale content
8. **Always close with `@conflict-auditor`** — required after any multi-file change session

---

## Source Repositories

- `Textbook/Chapter 1 - The Essentials.ipynb` — general
- `Textbook/Chapter 7 - Building an OLS Regression Model.ipynb` — general
- `ECON 411 611 Syllabus.docx` — general

---

## Style Rules

No project-specific style rules defined.
