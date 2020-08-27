#dictWithIndexAndKey.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
macro_dict = {"GDP":{},
              "Real GDP":{},
              "Price Level":{},
              "Money":{}}
#Nominal GDP = Price Level * Real GDP

# Price Level = Nominal GDP / Real GDP

for key in macro_dict:
    for i in range(1990, 2018):
        macro_dict[key][i] = np.random.random() * 10000

macro_DF = pd.DataFrame(macro_dict)
macro_DF["Price Level"] = macro_DF["GDP"] / macro_DF["Real GDP"]
macro_DF["Velocity"] = macro_DF["GDP"] / macro_DF["Money"]
print(macro_dict)
print(macro_DF)
macro_DF.plot.line(legend='right')

for key in macro_DF:
    macro_DF[key].plot.line()
    plt.title(key, fontsize=20)
    plt.show()
    plt.close()
