# Pandas Datareader Reference — LearnPythonStatsEcon

> Quick-reference for **Pandas Datareader** in LearnPythonStatsEcon.
> This is a lightweight reference file, not a full agent.

---

## Official Documentation

https://pandas-datareader.readthedocs.io/en/latest/

## Key API Surface

pdr.DataReader(name, data_source, start, end) — fetch time-series data; data_source options: 'fred' (FRED), 'yahoo' (Yahoo Finance), 'famafrench' (Fama-French), 'wb' (World Bank), 'oecd', 'eurostat'; pdr.fred.FredReader(symbols, start, end).read() — direct FRED access; pdr.wb.download(indicator, country, start, end) — World Bank data; Returns pandas DataFrame indexed by date

## Common Patterns & Pitfalls

Use pdr.DataReader('SERIES_ID', 'fred', start='2000-01-01') to fetch FRED series — SERIES_ID examples: 'GDP', 'CPIAUCSL', 'FEDFUNDS', 'UNRATE', 'M2SL'. Chain with .pct_change() or .diff() for growth rates. Pitfall: Yahoo Finance reader is unreliable — prefer yfinance for equity data. Pitfall: some data sources require an API key set as environment variable (e.g. FRED requires FRED_API_KEY for bulk requests). Wrap reads in try/except RemoteDataError for network resilience in notebooks.

## Key Conventions

- Follow project style rules when using Pandas Datareader
- Refer to authority sources for API contract accuracy

## Related Agents

- `@technical-validator` — verify technical accuracy of Pandas Datareader usage
- `@primary-producer` — implements code that depends on Pandas Datareader
