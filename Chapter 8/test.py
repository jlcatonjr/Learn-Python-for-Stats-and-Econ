import pandas as pd
import matplotlib.pyplot as plt
from linearmodels import PanelOLS

data = pd.DataFrame.from_csv("fraserDataWithRGDPPC.csv", index_col=[0,1], 
                             parse_dates = True)

# Panel OLS
# save dataframe with only the variables that will be used in regression
# and drop any observations that are missing any one of these values
reg_data = data[["RGDP Per Capita", "Sound Money", "Government Consumption", 
                 "SUMMARY INDEX"]].dropna()

reg_data["5 Year Lag"] = reg_data.groupby(level=0)["RGDP Per Capita"].shift(-5)
reg_data.to_csv("test.csv")