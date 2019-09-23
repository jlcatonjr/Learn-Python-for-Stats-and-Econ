import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("mpd2018.xlsx", sheet_name="Full data", index_col = [0,2])

years = []
country_list = []

for index in data.index:
    country_code = index[0]
    year = index[1]
    if country_code not in country_list: country_list.append(country_code)
    if year not in years: years.append(year)

years = sorted(years)


pairs_dict = {}
pairs_dict[0] = ["CAN", "FIN"]
pairs_dict[1] = ["FRA","DEU"]
pairs_dict[2] = ["GBR", "NLD"]
linestyles = ["-",":","--"]

for key in pairs_dict:
    country_pair = pairs_dict[key]    
    fig = plt.figure(figsize =(16,8))
    for i in range(len(country_pair)):
        country = country_pair[i]
        linestyle = linestyles[i]
        plt.plot(data.ix[(country),:]["cgdppc"].dropna(),
                         linestyle = linestyle, label=country)
    plt.xlim([1825,max(years)])
    plt.rcParams.update({'legend.fontsize': 25,'legend.handlelength': 2})
    plt.rcParams.update({'font.size': 25})
    plt.legend()
    plt.show()
    plt.close()