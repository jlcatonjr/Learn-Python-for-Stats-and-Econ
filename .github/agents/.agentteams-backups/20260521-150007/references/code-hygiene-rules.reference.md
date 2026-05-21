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

<!-- Example:
### CH-21 — Project-Specific Rule Name

**Category:** <category>
**Severity:** <severity>

Description and enforcement check.
-->
