<!-- AGENTTEAMS:BEGIN content v=1 -->
# Pandas Reference — LearnPythonStatsEcon

> Quick-reference for **Pandas ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`Pandas` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://pandas.pydata.org/docs/reference/

## Key API Surface

DataFrame/Series creation and I/O (pd.read_csv, pd.read_excel, to_csv); indexing (.loc, .iloc, boolean indexing); groupby, merge/join, pivot_table; time-series (DatetimeIndex, resample, rolling); string methods (.str.*); missing data (dropna, fillna, isna)

<!-- Document the primary classes, functions, or APIs that project code depends on from Pandas. -->

## Common Patterns & Pitfalls

Always set index explicitly after loading CSVs when a natural key exists. Use .copy() when slicing to avoid SettingWithCopyWarning. groupby().agg() for multi-stat summaries. pd.to_datetime() + dt accessor for time-series manipulation. Pitfall: chained indexing silently creates copies — use .loc.

<!-- Document common usage patterns, best practices, and known issues for Pandas . -->

## Key Conventions

- Follow project style rules when using Pandas
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of Pandas usage
- `@primary-producer` — implements code that depends on Pandas
<!-- AGENTTEAMS:END content -->
