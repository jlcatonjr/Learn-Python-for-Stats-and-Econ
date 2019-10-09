import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from linearmodels import PanelOLS

#import data
data = pd.DataFrame.from_csv("fraserDataWithRGDPPC.csv", index_col=[0,1], 
                             parse_dates = True)

# create list of each index set from multi index
years = list(sorted(set(data.index.get_level_values('Year'))))
country = list(sorted(set(data.index.get_level_values('ISO_Code'))))
#choose variables that will be plotted for each year in scatter
plot_vars = ["Sound Money", "Government Consumption", 
             "RGDP Per Capita","Quartile"]

# Normalize income so that 1 represents the maximum value of RGDP Per Capita
# This will allow dot to be easily adjusted
data["RGDP Per Capita"] = data["RGDP Per Capita"] / max(data["RGDP Per Capita"]) * 1000

# Panel OLS
reg_data = data[["RGDP Per Capita", "Sound Money", "Government Consumption", 
                 "SUMMARY INDEX"]].dropna()
x = reg_data[["Sound Money", "Government Consumption", 
              "SUMMARY INDEX"]]
y = reg_data[["RGDP Per Capita"]]
mod = PanelOLS(y, x, entity_effects=True, time_effects=False)
res = mod.fit(cov_type='clustered', cluster_entity=True)
print(res.summary)
