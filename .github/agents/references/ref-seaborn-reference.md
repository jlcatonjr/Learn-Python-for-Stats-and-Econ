<!-- AGENTTEAMS:BEGIN content v=1 -->
# seaborn Reference — LearnPythonStatsEcon

> Quick-reference for **seaborn ** (library) in LearnPythonStatsEcon.
> This is a lightweight reference file, not an agent. For operational procedures, consult the tool's reference/skill document, or escalate to `@orchestrator`.

---

## Version

`seaborn` ``

## Configuration

**Config files:** `N/A`

## Official Documentation

https://seaborn.pydata.org/api.html

## Key API Surface

Figure-level functions (sns.relplot, sns.displot, sns.catplot, sns.lmplot); axes-level functions (sns.scatterplot, sns.lineplot, sns.histplot, sns.kdeplot, sns.boxplot, sns.violinplot, sns.barplot, sns.heatmap, sns.pairplot); theming (sns.set_theme, sns.set_palette, sns.set_style); FacetGrid for multi-panel layout

<!-- Document the primary classes, functions, or APIs that project code depends on from seaborn. -->

## Common Patterns & Pitfalls

Call sns.set_theme() at the top of a notebook for consistent aesthetics. Pass tidy DataFrames via data=df with x='col', y='col' keyword arguments. Use hue= for colour-encoding a grouping variable. Seaborn is built on Matplotlib — use plt.tight_layout() and plt.savefig() as usual. Pitfall: seaborn expects long/tidy data — reshape wide DataFrames with pd.melt() first.

<!-- Document common usage patterns, best practices, and known issues for seaborn . -->

## Key Conventions

- Follow project style rules when using seaborn
- Refer to authority sources for API contract accuracy
- Validate changes against existing tests before committing

## Related Agents

- `@technical-validator` — verify technical accuracy of seaborn usage
- `@primary-producer` — implements code that depends on seaborn
<!-- AGENTTEAMS:END content -->
