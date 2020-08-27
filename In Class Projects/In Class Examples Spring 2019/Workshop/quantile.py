#quantile.py

import pandas as pd
import numpy as np

def create_quantile(n, data, year, quantile_var, quantile_name):
    # index that identifies countries for a given year
    year_index = data.index.get_level_values("Year") == year
    quantile_values_dict = {i:data[year_index][quantile_var]\
                .quantile(i/n) for i in range(1, n+1)}
    #cycle through each country for a given year
    for index in data[year_index].index:
        # identify value of the variable of interest
        val = data.ix[index][quantile_var]
        # compare that value to the values that divide each quantile
        for i in range(1, n + 1):
            # if the value is less than the highest in the quantile identified,
            # save quantile as i
            if val <= quantile_values_dict[i]:
                data[quantile_name][index] = i
                # exit loop
                break
            # otherwise check the highest value of the next quantile
            else:
                continue

#choose number of divisions
n = 5
#import data
data = pd.DataFrame.from_csv("fraserDataWithRGDPPC.csv", index_col=[0,1], 
                             parse_dates = True)
#Create column identifying n-tile rank
quantile_var = "RGDP Per Capita"
quantile_name = quantile_var + " " + str(n) + "-tile" 
data[quantile_name] = np.nan
years = list(sorted(set(data.index.get_level_values('Year'))))
for year in years:
    create_quantile(n, data, year, quantile_var, quantile_name)