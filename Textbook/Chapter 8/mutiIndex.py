# multiIndex.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# index_col = [0,2] will choose countrycode as primary index, and year as 
# secondary index
data = pd.read_excel("mpd2018.xlsx", sheet_name = "Full data", index_col = [0,2])
# create list of years to identify max extent of date range to plot
# First find list of all years in index
years = data.index.get_level_values('year')
# then remove any repeated observations
years = set(years)
# sort the years in numerical order
years = sorted(list(years))

#pairs of countries to compare in plots
pairs = [("CAN", "FIN"), ("FRA", "DEU"), ("GBR", "NLD")]
linestyles = ["-", ":"]

for pair in pairs:
    fig, ax = plt.subplots(figsize=(16,8))
    for i in range(len(pair)):
        country = pair[i]
        linestyle = linestyles[i]
        data.ix[country,:]["cgdppc"].dropna().plot.line(ax = ax,
               label = country, linestyle = linestyle)
    plt.xlim([1825, max(years)])
    plt.rcParams.update({"legend.fontsize": 25, "legend.handlelength": 2})
    plt.rcParams.update({"font.size": 25})
    plt.title("$Real$ $GDP$ $Per$ $Capita$", fontsize=36)
    plt.legend()
    plt.show()
    plt.close()
        