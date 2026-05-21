# Helipad Reference — LearnPythonStatsEcon

> Quick-reference for **Helipad** in LearnPythonStatsEcon.
> This is a lightweight reference file, not a full agent.

---

## Official Documentation

https://helipad.dev/apidocs/

## Key API Surface

Model class — main simulation container; model.addPrimitive(name, cls) — register agent type; model.addParam(name, title, type, dflt) — add adjustable parameter; model.addPlot(name, title) / model.addSeries() — define visualisation; model.start() / model.launchGUI() — run simulation; Agent base class with step() method; match() function for pairwise agent interactions

## Common Patterns & Pitfalls

Define agent behaviour by subclassing Agent and overriding step(). Use model.addPrimitive() to register each agent class before calling start(). Parameters added with addParam() appear as GUI sliders — set dflt for the default value. Collect time-series data via model.addPlot() and model.addSeries(). Pitfall: helipad's interactive GUI requires a Tkinter event loop — in Jupyter use model.start() rather than model.launchGUI().

## Key Conventions

- Follow project style rules when using Helipad
- Refer to authority sources for API contract accuracy

## Related Agents

- `@technical-validator` — verify technical accuracy of Helipad usage
- `@primary-producer` — implements code that depends on Helipad
