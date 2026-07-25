<!-- AGENTTEAMS:BEGIN content v=1 -->
# NumPy Reference — LearnPythonStatsEcon

> Quick-reference for **NumPy ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`NumPy` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://numpy.org/doc/stable/reference/

## Key API Surface

ndarray creation (np.array, np.zeros, np.ones, np.arange, np.linspace); array operations (reshape, transpose, concatenate, stack); math (np.sum, np.mean, np.std, np.dot, np.linalg); broadcasting and vectorized arithmetic

<!-- Document the primary classes, functions, or APIs that project code depends on from NumPy. -->

## Common Patterns & Pitfalls

Prefer vectorized operations over Python loops for performance. Use dtype=float64 explicitly when storing financial/econometric data. np.nan-safe aggregates: np.nanmean, np.nanstd. For boolean indexing: arr[arr > 0]. Pitfall: integer division in older NumPy — cast dtypes explicitly.

<!-- Document common usage patterns, best practices, and known issues for NumPy . -->

## Key Conventions

- Follow project style rules when using NumPy
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of NumPy usage
- `@primary-producer` — implements code that depends on NumPy
<!-- AGENTTEAMS:END content -->
