#dictWithIndexAndKey.py
import pandas as pd
import numpy as np

macro_dict = {"GDP":{},
             "Real GDP":{},
             "Price Level":{},
             "Money":{}}

for key in macro_dict:
    for i in range(1990,2018):
        macro_dict[key][i] = np.random.random()* 10000

print(macro_dict)
macro_DF = pd.DataFrame(macro_dict)
macro_DF["Velocity"] = macro_DF["Money"] / macro_DF["GDP"]
print(macro_DF)
print(macro_DF.loc[1995:2000])
print(macro_DF["Real GDP"].loc[1995:2000])
print(macro_DF.loc[1995:2000]["Real GDP"])



#import matplotlib.pyplot as plt
#macro_DF.plot.line(legend="best")
#plt.show()
#plt.close()
#
#for key in macro_DF:
#    macro_DF[key].plot.line()
#    plt.title(key,fontsize=20)
#    plt.show()
#    plt.close()