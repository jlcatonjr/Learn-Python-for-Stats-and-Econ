import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = pd.read_excel("mpd2018.xlsx", sheet_name="Full data", index_col = [0,2])
print(data)
# # create list of years to identify max extent of date range for plots
years = data.index.get_level_values('year')
years = set(years)
years = sorted(list(years))



# # pairs of countries to compare in plots
# pairs_dict = {}
# pairs_dict[0] = ("CAN", "FIN")
# pairs_dict[1] = ("FRA","DEU")
# pairs_dict[2] = ("GBR", "NLD")
# linestyles = ["-",":","--"]

# for key in pairs_dict:
#     country_pair = pairs_dict[key]    
#     fig = plt.figure(figsize =(16,8))
#     for i in range(len(country_pair)):
#         country = country_pair[i]
#         linestyle = linestyles[i]
#         plt.plot(data.ix[(country),:]["cgdppc"].dropna(),
#                          linestyle = linestyle, label=country)
#     plt.xlim([1825,max(years)])
#     plt.rcParams.update({'legend.fontsize': 25,'legend.handlelength': 2})
#     plt.rcParams.update({'font.size': 25})
#     plt.title("$Real$ $GDP$ $Per$ $Capita$", fontsize = 36)
#     plt.legend()
#     plt.show()
    # plt.close()