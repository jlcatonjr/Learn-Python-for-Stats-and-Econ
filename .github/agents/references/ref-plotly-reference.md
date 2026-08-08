<!-- AGENTTEAMS:BEGIN content v=1 -->
# plotly Reference — LearnPythonStatsEcon

> Quick-reference for **plotly ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`plotly` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://plotly.com/python-api-reference/

## Key API Surface

Plotly Express (px) — high-level: px.scatter, px.line, px.bar, px.histogram, px.box, px.heatmap, px.choropleth; Graph Objects (go) — low-level: go.Figure, go.Scatter, go.Bar, go.Heatmap, fig.add_trace(), fig.update_layout(), fig.update_xaxes(); Export: fig.show(), fig.write_html(), fig.write_image()

<!-- Document the primary classes, functions, or APIs that project code depends on from plotly. -->

## Common Patterns & Pitfalls

Use px for quick interactive charts; switch to go.Figure for fine-grained control. fig.show() renders inline in Jupyter — set pio.renderers.default='notebook' if blank. fig.update_layout(title=, xaxis_title=, yaxis_title=) for clean labelling. Export interactive charts with fig.write_html('chart.html'). Pitfall: Plotly figures are JSON-serialisable — very large datasets slow the browser.

<!-- Document common usage patterns, best practices, and known issues for plotly . -->

## Key Conventions

- Follow project style rules when using plotly
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of plotly usage
- `@primary-producer` — implements code that depends on plotly
<!-- AGENTTEAMS:END content -->
