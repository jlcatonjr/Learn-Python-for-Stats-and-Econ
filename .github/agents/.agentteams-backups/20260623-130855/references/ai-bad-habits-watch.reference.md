# AI Coding Bad-Habits Catalog — LearnPythonStatsEcon

<!-- AGENTTEAMS:BEGIN content v=1 -->
> Authoritative catalog of bad coding habits common across AI agents, mapped to
> corrective patterns. Consumed by `@code-hygiene` (CH-25) and `@security` when
> screening AI-authored or AI-edited code. Generated from the agentteams
> framework (source of truth: `agentteams/ai_bad_habits.py`); do not hand-edit.
> Refreshed on every team initialization and `--update --merge`.

**Scope:** code-quality, correctness, and process habits specific to AI
agents. Security-class habits (injection, secrets, excessive agency,
supply chain, unbounded consumption) are owned by `@security` and are
deliberately not catalogued here.

## Bad-habit catalog (BH-NN → corrective pattern)

### Code hygiene

| BH | Bad habit | Cross-link | Corrective pattern |
|----|-----------|------------|--------------------|
| BH-01 | Tutorial-style over-commenting of obvious syntax | — | Comment the why, not the what; no narrating obvious syntax |
| BH-02 | Stray print / console.log debug statements left in code | CH-04 | Use a structured logger, not print; strip debug output before commit |
| BH-03 | Single-use helper functions adding needless indirection | — | Inline single-use helpers; abstract only on the third repetition (rule of three) |
| BH-04 | Duplicated code blocks instead of reuse | CH-08 | Reuse existing utilities; extract a shared helper at 3 occurrences (DRY) |
| BH-05 | Tests omitted unless explicitly requested | CH-21 | Tests mandatory (happy path + edge/error cases); enforce a coverage gate |

### AI-specific correctness

| BH | Bad habit | Cross-link | Corrective pattern |
|----|-----------|------------|--------------------|
| BH-06 | Hallucinated or unresolvable dependencies / imports | — | Verify every import and package resolves against the real registry; pin + lockfile. (The supply-chain / slopsquatting SECURITY angle is @security's.) |
| BH-07 | Model output forwarded without shape-validation | CH-23 | Validate/shape-check AI output and fail fast on unexpected shapes (CH-23). (The untrusted-sink injection angle is @security's.) |

### Process

| BH | Bad habit | Cross-link | Corrective pattern |
|----|-----------|------------|--------------------|
| BH-08 | Forces a solution on ambiguity instead of asking | — | Plan-first; list assumptions and open questions before coding |
| BH-09 | 'Make it better' refinement loops accumulate flaws | — | Re-review and re-test after every iteration, not just at the end |
<!-- AGENTTEAMS:END content -->
