import string
import random
import pandas as pd
import numpy as np
print(string.ascii_uppercase)
quartile_dict = {}

for i in string.ascii_uppercase:
    quartile_dict[i] = [random.randint(0, 1000)]
    quartile_dict[i.lower()] = [random.randint(0, 1000)]
#quartile_dict = sorted(quartile_dict.items(), key=operator.itemgetter(1))

quartile_DF = pd.DataFrame(quartile_dict).T
quartile_DF = quartile_DF.rename(columns={0:"Values"})
quartile_DF = quartile_DF.sort_values(by=["Values"])
print(quartile_DF)

quartile_values_dict = {1:quartile_DF.quantile(.25).values[0],
                        2:quartile_DF.quantile(.5).values[0],
                        3:quartile_DF.quantile(.75).values[0]}
print(quartile_values_dict)
quartile_DF["Quartile"] = np.nan

for index in quartile_DF.index:
    print(index)
    val = quartile_DF.ix[index]["Values"]

    if val <= quartile_values_dict[1]:
        quartile_DF["Quartile"][index] = 1
    elif val <= quartile_values_dict[2]:
        quartile_DF["Quartile"][index] = 2
    elif val <= quartile_values_dict[3]:
        quartile_DF["Quartile"][index] = 3
    else:
        quartile_DF["Quartile"][index] = 4
print(quartile_DF["Quartile"].value_counts())    