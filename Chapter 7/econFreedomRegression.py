#econFreedomRegression
import pandas as pd
import regression
import statsmodels.api as sm

data = pd.read_csv("cleanedEconFreedomData.csv")
reg = regression.Regression()

y_var = ["GDP per Capita (PPP)"]
x_vars_unrestricted = ["Judical Effectiveness", "Property Rights",
          "Fiscal Health"]#, "Investment Freedom ", "Financial Freedom", 
#          "Inflation (%)", "Public Debt (% of GDP)"]
x_vars_restricted = ["Judical Effectiveness"]
X = data[x_vars_unrestricted]
X = sm.add_constant(X)
Y = data[y_var]
res = sm.OLS(Y, X).fit()

reg.OLS("GDP Per Capita Restricted", data, y_var, x_vars_restricted)
reg.OLS("GDP Per Capita Unrestricted", data, y_var, x_vars_unrestricted)

#
joint_f_test = reg.joint_f_test("GDP Per Capita Unrestricted", 
                                "GDP Per Capita Restricted")
print(joint_f_test)
print(res.f_test("Property Rights = Fiscal Health = 0"))