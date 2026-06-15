# Ipywidgets Reference — LearnPythonStatsEcon

> Quick-reference for **Ipywidgets** in LearnPythonStatsEcon.
> This is a lightweight reference file, not a full agent.

---

## Official Documentation

https://ipywidgets.readthedocs.io/en/stable/

## Key API Surface

widgets.IntSlider / FloatSlider(value, min, max, step) — numeric sliders; widgets.Dropdown(options, value) — dropdown selector; widgets.Checkbox(value) — boolean toggle; widgets.Output() — capture display output; widgets.HBox / VBox(*children) — layout containers; interact(fn, **kwargs) / interactive(fn, **kwargs) — auto-generate UI from function signature; widgets.observe(handler, names) — react to value changes; display(widget) — render widget in notebook

## Common Patterns & Pitfalls

Use interact() or @interact decorator for quick exploratory UIs — pass slider ranges as (min, max) or (min, max, step) tuples. For more control use interactive() and display its .widget attribute. Combine multiple widgets with HBox/VBox for layout. Use widgets.Output() context manager to capture prints/plots inside callbacks. Pitfall: widgets only render in a live Jupyter kernel — use Voilà to serve them as standalone apps or nbconvert --to html for static export. Pitfall: observe callbacks fire on every keystroke for Text widgets — debounce with a submit Button or use continuous_update=False on sliders.

## Key Conventions

- Follow project style rules when using Ipywidgets
- Refer to authority sources for API contract accuracy

## Related Agents

- `@technical-validator` — verify technical accuracy of Ipywidgets usage
- `@primary-producer` — implements code that depends on Ipywidgets
