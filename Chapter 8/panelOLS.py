import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from linearmodels import PanelOLS

#import data
data = pd.DataFrame.from_csv("fraserDataWithRGDPPC.csv", index_col=[0,1], 
                             parse_dates = True)
data["RGDP Per Capita Lag 5"] = data.groupby(level=0)["RGDP Per Capita"].shift(-5)
data["RGDP Per Capita Growth Rate"] = \
    data.groupby(level=0)["RGDP Per Capita"].pct_change(-1)
data["RGDP Per Capita 5 Year Growth Rate"] = \
    data.groupby(level=0)["RGDP Per Capita"].pct_change(-5)

data["Log RGDP Per Capita"] = np.log(data["RGDP Per Capita"])
data["Log RGDP Per Capita Lag 5"] =  \
    data.groupby(level=0)["Log RGDP Per Capita"].shift(-5)
new_vars = ["RGDP Per Capita Lag 5", "RGDP Per Capita Growth Rate",\
    "RGDP Per Capita 5 Year Growth Rate", "Log RGDP Per Capita",\
    "Log RGDP Per Capita Lag 5"]

# Panel OLS
# save dataframe with only the variables that will be used in regression
# and drop any observations that are missing any one of these values
#reg_data = data[["RGDP Per Capita", "Sound Money", "Government Consumption", 
#                 "SUMMARY INDEX",] + new_vars]

reg_data = data[["Log RGDP Per Capita", "Log RGDP Per Capita Lag 5", 
                 "Sound Money", "Government Consumption", "SUMMARY INDEX"]]
# RGDP Per Capita is the dependent variable
y_name = ["Log RGDP Per Capita"]
# Sound Money, Government Consumption, and SUMMARY INDEX are our indep vars
x_names = ["Sound Money", "Government Consumption", "SUMMARY INDEX", 
           "Log RGDP Per Capita Lag 5"]
# save dependent and independent variables as their own objects
y = reg_data[y_name]
x = reg_data[x_names]

# prepare panelOLS controlling for entity fixed effects
mod = PanelOLS(y, x, entity_effects=True, time_effects=False)
# estimate with robust errors
res = mod.fit(cov_type='clustered', cluster_entity=True)
#save predictor and place values in the original dataframe named data
predictor = res.predict()
predict_name = y_name[0] + " Predict"
data[predict_name] = predictor

years = list(sorted(set(data.index.get_level_values('Year'))))
country_list = list(sorted(set(data.index.get_level_values('ISO_Code'))))
plt.rcParams.update({'legend.fontsize': 25,'legend.handlelength': 2})
plt.rcParams.update({'font.size': 20})
for year in years:
    fig, ax = plt.subplots(figsize = (12,8))
    year_index = data.index.get_level_values("Year") == year
  
    data[year_index].plot.scatter(x = "Government Consumption", 
        y = y_name[0] + " Predict", c = "C0", s = 100, ax = ax, 
        legend = True, label= "Predict")
    data[year_index].plot.scatter(x = "Government Consumption", 
        y = y_name[0], c = "C1", s = 100, ax = ax, label = "Observed")
    plt.title(str(year)[:4], fontsize = 36)
    plt.show()
    plt.close()
    
for country in country_list:
    fig, ax = plt.subplots(figsize = (12,8))
    country_index = data.index.get_level_values("ISO_Code") == country
    df = data[country_index].sort_values(by="Year")
    df.to_csv("tempDF.csv")
    df = pd.read_csv("tempDF.csv", index_col = ["Year"])
    
    xticks = list(sorted(set(df.index.get_level_values('Year'))))
    xticks = [str(tick)[:4] for tick in xticks]
    df[y_name[0] + " Predict"].plot.line(c="C0",
        ax = ax, label = "Predictor")
    df[y_name[0]].plot.line(c="C1", ax = ax, 
        label = "Observation")
#    ax.set_xticks(df.index)
#    ax.set_xticklabels(xticks)
    ax.tick_params(axis = "x", rotation = 90)
    ax.set_xlabel("Year")
    plt.title(country, fontsize = 36)
    plt.legend()
    plt.show()
    plt.close()
    