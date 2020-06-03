#panelRegression.py
import pandas as pd
import numpy as np
import datetime
import regression

# import data
data = pd.read_csv("fraserDataWithRGDPPC.csv", index_col = ["ISO_Code", "Year"], 
                   parse_dates = True)
data["RGDP Per Capita Lag"] = data.groupby(level="ISO_Code")\
    ["RGDP Per Capita"].shift(-1)
data = data[data.index.get_level_values("Year") > datetime.datetime(2000,1,1)]

for key in data:
    if "GDP" in key:
        data["Log " + key] = np.log(data[key])
# We do not want to difference the index values, only the Real GDP values
# so initialize the diff data as teh dataframe but only include index values
# from a differenced matrix (one year of observations will be missing)
diff_index = data.groupby(level=0).diff(-1).dropna().index
data_dict = {}
data_dict["Data"] = data
data_dict["Diff Data"] = data.copy().loc[diff_index]
for key in data:
    if "GDP" in key:
        data_dict["Diff Data"][key] = data[key].groupby(level=0).diff(-1)
data_dict["Diff Data"] = data_dict["Diff Data"].dropna()

# prepare regression variables
X_names = ["EFW", "Log RGDP Per Capita Lag"]
y_name = ["Log RGDP Per Capita"]

# save instance of regression class
reg = regression.Regression()
for key in data_dict:
    # call OLS and Panel for comparison
    data = data_dict[key]
    reg.OLS(reg_name = key, data = data.dropna(),
            y_name = y_name, beta_names = X_names)
    print(key, reg.estimates, sep = "\n")
    print(reg.stats_DF)
    panel_name = key + " panel"
    reg.panel_regression(reg_name = panel_name, data = data.dropna(),
            y_name = y_name, X_names = X_names, entity = True, time = False)
    print(key, reg.estimates, sep = "\n")
    print(reg.stats_DF)    
    joint_f_test = reg.joint_f_test(key, key + " panel")
    joint_f_test.to_csv(key + " panel comparison.csv")
    print()