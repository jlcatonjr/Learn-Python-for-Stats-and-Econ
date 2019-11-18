#indicatorRegression.py
import pandas as pd
import numpy as np
import datetime
import regression

def create_indicator_variable(data, indicator_name, index_name, 
                              target_index_list):
    # Prepare column with name of indicator variable
    data[indicator_name] = 0
    # for each index whose name matches an entry in target_index_list
    # a value of 1 will be recorded
    for index in target_index_list:
        data[indicator_name].loc[data.index.get_level_values(\
            index_name) == index] = 1

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

# Create indicator variable for North Amierca in both data and diff_data
indicator_name = "North America"
index_name = "ISO_Code"
countries_in_north_america = ["BHS", "BRB", "BLZ", "CAN", "CRI", "DOM", "SLV",
                              "GTM", "HTI", "HND", "JAM", "MEX", "NIC", "PAN",
                              "TTO", "USA"]
for key in data_dict:
    data = data_dict[key]
    create_indicator_variable(data = data, indicator_name = indicator_name,
        index_name = index_name,target_index_list = countries_in_north_america)

# prepare regression variables
X_names = ["EFW", "Log RGDP Per Capita Lag", "North America"]
y_name = ["Log RGDP Per Capita"]

# save instance of regression class
reg = regression.Regression()
for key in data_dict:
    # call OLS method
    data = data_dict[key]
    reg.OLS(reg_name = key, data = data.dropna(),
            y_name = y_name, beta_names = X_names)
    print(key, reg.estimates, sep = "\n")
    print(reg.stats_DF)
    print()