#logAndDifferenceData.py
import pandas as pd
import numpy as np
import datetime
# import data
data = pd.read_csv("fraserDataWithRGDPPC.csv", index_col = ["ISO_Code", "Year"],
                   parse_dates = True)

data["RGDP Per Capita Lag"] = data.groupby(level = "ISO_Code")\
    ["RGDP Per Capita"].shift(-1)
data = data[data.index.get_level_values("Year") > datetime.datetime(2000, 1, 1)]

log_vars = [key for key in data if "GDP" in key]
data[["Log " + key for key in log_vars]] = np.log(data[[key for key in log_vars]])

# We do not want to difference the index values, only the Real GDP values
# so initialize the diff data as the dataframe, but only include index values
# from a differenced matrix
diff_index = data.groupby(level=0).diff(-1).dropna().index
data_dict = {}
data_dict["Data"] = data
data_dict["Diff Data"] = data.copy().loc[diff_index]
for key in data:
    if "GDP" in key:
        data_dict["Diff Data"][key] = data[key].groupby(level=0).diff(-1)
data_dict["Diff Data"] = data_dict["Diff Data"].dropna()