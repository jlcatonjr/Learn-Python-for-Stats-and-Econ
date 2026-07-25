<!-- AGENTTEAMS:BEGIN content v=1 -->
# Jupyter Reference — LearnPythonStatsEcon

> Quick-reference for **Jupyter ** (framework) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`Jupyter` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://docs.jupyter.org/en/latest/

## Key API Surface

IPython display API (display, HTML, Markdown, Image); magic commands (%matplotlib inline, %run, %%time, %who); Jupyter widgets (ipywidgets); nbformat for programmatic notebook I/O

<!-- Document the primary classes, functions, or APIs that project code depends on from Jupyter. -->

## Common Patterns & Pitfalls

Use %matplotlib inline or %matplotlib widget at notebook top. Cell execution order matters — restart kernel and run all before submitting. Use display(df) instead of print(df) for formatted DataFrame rendering. Pitfall: hidden state from out-of-order execution causes hard-to-reproduce bugs.

<!-- Document common usage patterns, best practices, and known issues for Jupyter . -->

## Key Conventions

- Follow project style rules when using Jupyter
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of Jupyter usage
- `@primary-producer` — implements code that depends on Jupyter
<!-- AGENTTEAMS:END content -->
