#econFreedomRegression
import pandas as pd
import regression

data = pd.read_csv("cleanedEconFreedomData.csv")
reg = regression.Regression()

y_var = ["GDP per Capita (PPP)"]
x_vars_unrestricted = ["Trade Freedom", "Property Rights", "Judical Effectiveness", 
          "Fiscal Health", "Investment Freedom ", "Financial Freedom", 
          "Inflation (%)", "Public Debt (% of GDP)"]
x_vars_restricted = ["Property Rights", "Judical Effectiveness"]

reg.OLS("GDP Per Capita Unrestricted", data, y_var, x_vars_unrestricted)
reg.OLS("GDP Per Capita Restricted", data, y_var, x_vars_restricted)


joint_f_test = reg.joint_f_test("GDP Per Capita Unrestricted", 
                                "GDP Per Capita Restricted")