#pandasSeriesVsDataFrame.py
import numpy as np
import pandas as pd

dataDict = {"range":np.arange(10)}
dataSeries = pd.Series(dataDict)
print(dataSeries)
print(dataSeries["range"])

dataDF=pd.DataFrame(dataDict)
print(dataDF)
print(dataDF["range"])
print(dataDF["range"][5:9])
#print(dataDF.loc[5:9])