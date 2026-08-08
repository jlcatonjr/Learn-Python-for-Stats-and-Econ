<!-- AGENTTEAMS:BEGIN content v=1 -->
# ipywidgets Reference — LearnPythonStatsEcon

> Quick-reference for **ipywidgets ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`ipywidgets` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://ipywidgets.readthedocs.io/en/stable/

## Key API Surface

widgets.IntSlider / FloatSlider(value, min, max, step) — numeric sliders; widgets.Dropdown(options, value) — dropdown selector; widgets.Checkbox(value) — boolean toggle; widgets.Output() — capture display output; widgets.HBox / VBox(*children) — layout containers; interact(fn, **kwargs) / interactive(fn, **kwargs) — auto-generate UI from function signature; widgets.observe(handler, names) — react to value changes; display(widget) — render widget in notebook

<!-- Document the primary classes, functions, or APIs that project code depends on from ipywidgets. -->

## Common Patterns & Pitfalls

Use interact() or @interact decorator for quick exploratory UIs — pass slider ranges as (min, max) or (min, max, step) tuples. For more control use interactive() and display its .widget attribute. Combine multiple widgets with HBox/VBox for layout. Use widgets.Output() context manager to capture prints/plots inside callbacks. Pitfall: widgets only render in a live Jupyter kernel — use Voilà to serve them as standalone apps or nbconvert --to html for static export. Pitfall: observe callbacks fire on every keystroke for Text widgets — debounce with a submit Button or use continuous_update=False on sliders.

<!-- Document common usage patterns, best practices, and known issues for ipywidgets . -->

## Key Conventions

- Follow project style rules when using ipywidgets
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of ipywidgets usage
- `@primary-producer` — implements code that depends on ipywidgets
<!-- AGENTTEAMS:END content -->
