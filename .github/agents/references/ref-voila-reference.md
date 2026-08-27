<!-- AGENTTEAMS:BEGIN content v=1 -->
# voila Reference — LearnPythonStatsEcon

> Quick-reference for **voila ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`voila` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://voila.readthedocs.io/en/stable/

## Key API Surface

CLI: voila notebook.ipynb — serve notebook as web app; voila --port=8866 --no-browser notebook.ipynb — specify port; voila --template=material notebook.ipynb — apply theme; voila --strip_sources=True — hide source cells in output; binder integration via postBuild + voila server extension; Python API: VoilaConfiguration for programmatic config

<!-- Document the primary classes, functions, or APIs that project code depends on from voila. -->

## Common Patterns & Pitfalls

Convert any ipywidgets notebook to a dashboard with `voila notebook.ipynb`. For Binder deployment add `voila` to requirements.txt and set URL path to `/voila/render/notebook.ipynb` in the Binder badge URL. Use --strip_sources=True for student-facing dashboards to hide code cells. Pitfall: Voilà re-executes the entire notebook on each page load — cache expensive computations or use @lru_cache on data-loading functions. Pitfall: widgets that depend on display() must use widgets.Output() — bare matplotlib plt.show() calls may not render correctly under Voilà.

<!-- Document common usage patterns, best practices, and known issues for voila . -->

## Key Conventions

- Follow project style rules when using voila
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of voila usage
- `@primary-producer` — implements code that depends on voila
<!-- AGENTTEAMS:END content -->
