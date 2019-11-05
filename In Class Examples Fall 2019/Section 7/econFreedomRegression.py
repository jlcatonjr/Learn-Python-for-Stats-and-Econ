#econFreedomRegression
import pandas as pd
import regression

data = pd.read_csv("cleanedEconFreedomData.csv", index_col = [0])
reg = regression.Regression()

y_var = ["GDP per Capita (PPP)"]
x_vars = ["Trade Freedom", "Property Rights", "Judical Effectiveness",
         "Fiscal Health", "Investment Freedom ", "Financial Freedom",
         "Inflation (%)", "Public Debt (% of GDP)"]

reg.OLS("GDP Per Capita", data, y_var, x_vars)