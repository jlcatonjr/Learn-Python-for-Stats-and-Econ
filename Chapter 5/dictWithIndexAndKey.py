#dictWithIndexAndKey.py
import pandas as pd
import numpy as np

macroDict = {"GDP":{},
             "Real GDP":{},
             "Price Level":{},
             "Money":{}}

for key in macroDict:
    for i in range(1990,2018):
        macroDict[key][i] = np.random.random()* 10000

print(macroDict)
macroDF = pd.DataFrame(macroDict)
macroDF["Velocity"] = macroDF["Money"] / macroDF["GDP"]
print(macroDF)

#print(macroDF.loc[1995:2000])
