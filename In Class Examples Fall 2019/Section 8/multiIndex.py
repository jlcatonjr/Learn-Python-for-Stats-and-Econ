#multiIndex.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# index_col = [0,2] will choose countrycodde as primary index, and year as
# secondary index
data = pd.read_excel("mpd2018.xlsx", sheet_name = "Full data", 
                     index_col = [0,2])
data = data.sort_index()


# create list of years to identify max extent of date range to plot
# First find list of all years in index
years = data.index.get_level_values("year")
#then remove any repeated observations
years = set(years)
# sort the sears in numerical order
years = sorted(list(years))
print(years)

#pairs of countries to compare in plots
pairs = [("CAN", "FIN"), ("FRA", "DEU"), ("GBR", "NLD")]
linestyles = ["-", ":"]

for pair in pairs:
    # for each pair, create a new plot
    fig, ax = plt.subplots(figsize = (24, 16))
    # cycle through index values in pair tuple
    for i in range(len(pair)):
        # choose country
        country = pair[i]
        # choose linestyle
        linestyle = linestyles[i]
        data.ix[country, :]["cgdppc"].dropna().plot.line(ax = ax,
               label = country, linestyle =linestyle, linewidth = 3)
    plt.xlim([1825, max(years)])
    plt.rcParams.update({"legend.fontsize": 30, "legend.handlelength": 2})
    plt.rcParams.update({"font.size":30})
    plt.title("$Real$ $GDP$ $Per$ $Capita$")
    plt.legend()
        
        
        
        
        
        
        
        
        