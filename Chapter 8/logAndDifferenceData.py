#logAndDifferenceData.py
import pandas as pd
import datetime
import numpy as np

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
data_dict["Diff Data"] = data.groupby(level=0).diff(-1).dropna()