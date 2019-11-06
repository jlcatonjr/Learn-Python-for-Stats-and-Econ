#indicatorRegression.py
import pandas as pd
import datetime
import numpy as np
import regression

def create_indicator_variable(data, indicator_name, index_name, target_index_list):
    # Prepare column with name of indicator variable
    data[indicator_name] = 0
    # for each index whose name matches an entry in target_index_list
    # a value of 1 will be recorded
    for index in target_index_list:
        data[indicator_name].loc[(data.index.get_level_values(\
            index_name)== index)] = 1

# Import data with "ISO_Code" and "Year" as index columns
data = pd.DataFrame.from_csv("fraserDataWithRGDPPC.csv", 
         index_col=[0,1], parse_dates = True)
data["RGDP Per Capita Lag"] = data.groupby(level=0)["RGDP Per Capita"].shift(-1)
data = data[data.index.get_level_values("Year") > datetime.datetime(1999,1,1)]

for key in data:
    if "GDP" in key:
        data["Log " + key] = np.log(data[key])

# place dataframe in dictionary
# this will increase efficiency of managing differenced data
data_dict = {}
data_dict["Data"] = data
data_dict["Diff Data"] = data.copy().loc[data.groupby(level=0).diff(-1).dropna().index]
for key in data:
    if "GDP" in key:
        data_dict["Diff Data"][key] = data[key].groupby(level=0).diff(-1)
data_dict["Diff Data"] = data_dict["Diff Data"].dropna()
#
#Create indicator variable for North America in both data and diff_data
indicator_name = "North America"
index_name = "ISO_Code"
countries_in_north_america = ["BHS", "BRB", "BLZ", "CAN", "CRI", "DOM",
                              "SLV", "GTM", "HTI", "HND", "JAM", "MEX",
                              "NIC", "PAN", "PAN", "TTO", "USA"]
for key in data_dict:
    create_indicator_variable(data_dict[key], indicator_name, index_name,
                          countries_in_north_america)
    
# prepare regression variables
X_names = ["SUMMARY INDEX", "Log RGDP Per Capita Lag", "North America"]
y_name = ["Log RGDP Per Capita"]

reg = regression.Regression()
for key in data_dict:
    #save instance of regression class
    # call regression method
    reg.OLS(reg_name = key, data = data_dict[key].dropna(), 
                y_name = y_name, beta_names = X_names,)
    print(key + "\n", reg.estimates)
    print(reg.stats_DF)
    print()