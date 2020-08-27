#quantile.py
import string
import random
import pandas as pd
import numpy as np

def create_quantile(n, data, category):
    quantile_values_dict = \
        {i:quantile_DF.quantile(i/n).values[0] for i in range(1, n+1)}
    quantile = category + " " + str(n) + "-tile" 
    data[quantile] = np.nan
    for index in data.index:
        val = quantile_DF.ix[index][category]
        for i in range(1, n + 1):
            if val <= quantile_values_dict[i]:
                quantile_DF[quantile][index] = i
                break
            else:
                continue
        
dct = {}
#choose number of divisions
n = 5
#create dictionary with random values
#use ascii characters as keys
for i in string.ascii_uppercase:
    dct[i] = [random.randint(0, 1000)]
    dct[i.lower()] = [random.randint(0, 1000)]

#transform dictionary to dataframe, transpose dataframe
quantile_DF = pd.DataFrame(dct).T
#name column as "Values"
quantile_DF = quantile_DF.rename(columns={0:"Values"})
#Create column identifying n-tile rank
create_quantile(n, quantile_DF, "Values")
# sort dataframe by "Values"
quantile_DF = quantile_DF.sort_values(by=["Values"])
print(quantile_DF)