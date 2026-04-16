# Statsmodels Reference — LearnPythonStatsEcon

> Quick-reference for **Statsmodels ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not a full agent. For tool-specific operations, consult the relevant specialist agent or escalate to `@orchestrator`.

---

## Version

`Statsmodels` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://www.statsmodels.org/stable/api.html

## Key API Surface

OLS regression (sm.OLS, smf.ols); GLM (sm.GLM); time-series models (ARIMA, SARIMAX, VAR); diagnostic tests (acf/pacf, Durbin-Watson, Breusch-Pagan, White test); summary tables (.summary(), .summary2()); formula interface (smf.ols('y ~ x1 + x2', data=df).fit())


## Common Patterns & Pitfalls

Always call .fit() — the model object alone is not fitted. Use smf formula interface for clean model specification with categorical dummies. model.summary() prints LaTeX-ready tables. Use HC3 robust standard errors: .fit(cov_type='HC3'). Pitfall: sm.add_constant(X) must be called explicitly when using sm.OLS with arrays.


## Key Conventions

- Follow project style rules when using Statsmodels
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of Statsmodels usage
- `@primary-producer` — implements code that depends on Statsmodels
