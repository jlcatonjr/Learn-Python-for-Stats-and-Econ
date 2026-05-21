# Plotly Reference — LearnPythonStatsEcon

> Quick-reference for **Plotly** in LearnPythonStatsEcon.
> This is a lightweight reference file, not a full agent.

---

## Official Documentation

https://plotly.com/python-api-reference/

## Key API Surface

Plotly Express (px) — high-level: px.scatter, px.line, px.bar, px.histogram, px.box, px.heatmap, px.choropleth; Graph Objects (go) — low-level: go.Figure, go.Scatter, go.Bar, go.Heatmap, fig.add_trace(), fig.update_layout(), fig.update_xaxes(); Export: fig.show(), fig.write_html(), fig.write_image()

## Common Patterns & Pitfalls

Use px for quick interactive charts; switch to go.Figure for fine-grained control. fig.show() renders inline in Jupyter — set pio.renderers.default='notebook' if blank. fig.update_layout(title=, xaxis_title=, yaxis_title=) for clean labelling. Export interactive charts with fig.write_html('chart.html'). Pitfall: Plotly figures are JSON-serialisable — very large datasets slow the browser.

## Key Conventions

- Follow project style rules when using Plotly
- Refer to authority sources for API contract accuracy

## Related Agents

- `@technical-validator` — verify technical accuracy of Plotly usage
- `@primary-producer` — implements code that depends on Plotly
