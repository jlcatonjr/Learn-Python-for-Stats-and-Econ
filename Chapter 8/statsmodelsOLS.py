#statsmodelsOLS.py
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt

data = pd.read_csv("cleanedEconFreedomData.csv", index_col = ["Country Name"])
y_var = ["5 Year GDP Growth Rate (%)"]
x_vars = ["Gov't Expenditure % of GDP ", "2017 Score", 
          "Population (Millions)", "Property Rights", "Business Freedom"]

y = data[y_var]
X = data[x_vars]
X["Constant"] = 1
results = sm.OLS(y, X).fit()
print(X.keys())
restricted_results = sm.OLS(y, X.drop(x_vars[1:], axis = 1)).fit()    
print(results.compare_f_test(restricted_results))

betaParams = results.params
tStats = results.tvalues
pValues =  results.pvalues
stdErrors = results.bse

resultsDict = {"Beta Estimates": betaParams,
               "t-stats": tStats,
               "p-values": pValues,
               "Standard Errors": stdErrors}
resultsDF = pd.DataFrame(resultsDict)
OLSSummary = results.summary()

predictor = results.predict()

data[y_var[0] + " Predictor"] = predictor
fig, ax = plt.subplots(figsize = (12,8))
plt.rcParams.update({"font.size": 18})
data.plot.scatter(x = y_var[0], y = y_var[0] + " Predictor", ax = ax)