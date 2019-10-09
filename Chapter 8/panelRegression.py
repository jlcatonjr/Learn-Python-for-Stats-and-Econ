#panelRegression.py
import pandas as pd
import datetime
import numpy as np
import regression

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
data_dict["Observed"] = data
data_dict["Differenced"] = data.groupby(level=0).diff(-1).dropna()


for key in data_dict:
    restrict_name ="Restricted Econ Freedom Panel Reg"
    unrestrict_name = "Unrestricted Econ Freedom Panel Reg"
    # prepare restricted regression variables
    X_names = ["RGDP Per Capita Lag"]
    y_name = ["RGDP Per Capita"]
    reg = regression.Regression()
    reg.panel_regression(reg_name = restrict_name, data = data_dict[key].dropna(),
            y_name = y_name, X_names = X_names, entity=True)

    print(key + "\n", reg.estimates)
    print(reg.stats_DF)
    # prepare restricted regression variables    
    X_names = ["SUMMARY INDEX", "RGDP Per Capita Lag"]
    y_name = ["RGDP Per Capita"]
    # create new column of data to mark countries that are in North America
    reg.panel_regression(reg_name = unrestrict_name, data = data_dict[key].dropna(),
            y_name = y_name, X_names = X_names, entity=True)

  
    print(key + "\n", reg.estimates)
    print(reg.stats_DF)
    print()
    fstat = reg.calculate_generalized_fstat(restrict_name, unrestrict_name)
    print("Null Hypothesis: Econ Freedom Doesn't Matter:\n", key, fstat)