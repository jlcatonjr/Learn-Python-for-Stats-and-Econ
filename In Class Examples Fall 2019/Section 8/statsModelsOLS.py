#statsmodelsOLS.py
import pandas as pd
import statsmodels.api as sm

data = pd.read_csv("cleanedEconFreedomData.csv", index_col = ["Country Name"])

y_var = ["GDP per Capita (PPP)"]

x_vars = ["Trade Freedom", "Property Rights", "Judical Effectiveness",]
#         "Fiscal Health", "Investment Freedom ", "Financial Freedom",
#         "Inflation (%)", "Public Debt (% of GDP)"]

y = data[y_var]
X = data[x_vars]
X["Constant"] = 1
results = sm.OLS(y, X).fit()

betaEstimates = results.params
tStats = results.tvalues
pValues = results.pvalues
stdErrors = results.bse

resultsDict = {"Beat Estimates": betaEstimates,
               "t-stats": tStats,
               "p-values": pValues,
               "Standard Errors": stdErrors
               }

resultsDF = pd.DataFrame(resultsDict)
print(resultsDF)
