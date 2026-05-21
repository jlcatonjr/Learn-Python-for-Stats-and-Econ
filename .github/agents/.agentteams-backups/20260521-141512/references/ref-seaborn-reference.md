# Seaborn Reference — LearnPythonStatsEcon

> Quick-reference for **Seaborn** in LearnPythonStatsEcon.
> This is a lightweight reference file, not a full agent.

---

## Official Documentation

https://seaborn.pydata.org/api.html

## Key API Surface

Figure-level functions (sns.relplot, sns.displot, sns.catplot, sns.lmplot); axes-level functions (sns.scatterplot, sns.lineplot, sns.histplot, sns.kdeplot, sns.boxplot, sns.violinplot, sns.barplot, sns.heatmap, sns.pairplot); theming (sns.set_theme, sns.set_palette, sns.set_style); FacetGrid for multi-panel layout

## Common Patterns & Pitfalls

Call sns.set_theme() at the top of a notebook for consistent aesthetics. Pass tidy DataFrames via data=df with x='col', y='col' keyword arguments. Use hue= for colour-encoding a grouping variable. Seaborn is built on Matplotlib — use plt.tight_layout() and plt.savefig() as usual. Pitfall: seaborn expects long/tidy data — reshape wide DataFrames with pd.melt() first.

## Key Conventions

- Follow project style rules when using Seaborn
- Refer to authority sources for API contract accuracy

## Related Agents

- `@technical-validator` — verify technical accuracy of Seaborn usage
- `@primary-producer` — implements code that depends on Seaborn
