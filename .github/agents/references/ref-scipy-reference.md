<!-- AGENTTEAMS:BEGIN content v=1 -->
# SciPy Reference — LearnPythonStatsEcon

> Quick-reference for **SciPy ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`SciPy` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://docs.scipy.org/doc/scipy/reference/

## Key API Surface

scipy.stats — probability distributions (norm, t, f, chi2, binom), hypothesis tests (ttest_ind, ttest_rel, mannwhitneyu, chi2_contingency, f_oneway), descriptive stats (describe, skew, kurtosis); scipy.optimize — minimize, curve_fit, root_scalar; scipy.linalg — solve, inv, det, eig

<!-- Document the primary classes, functions, or APIs that project code depends on from SciPy. -->

## Common Patterns & Pitfalls

scipy.stats.norm.cdf/ppf for z-score and critical-value lookups. ttest_ind(a, b, equal_var=False) (Welch t-test) unless variances are verified equal. f_oneway(*groups) for one-way ANOVA. Pitfall: most distribution objects use scale (not variance) as the second parameter.

<!-- Document common usage patterns, best practices, and known issues for SciPy . -->

## Key Conventions

- Follow project style rules when using SciPy
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of SciPy usage
- `@primary-producer` — implements code that depends on SciPy
<!-- AGENTTEAMS:END content -->
