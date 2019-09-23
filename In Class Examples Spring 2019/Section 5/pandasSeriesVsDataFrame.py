#pandasSeriesVsDataFrame.py
import numpy as np
import pandas as pd

data_dict = {"range": np.arange(10)}
data_series = pd.Series(data_dict)
series = pd.Series(np.arange(10))
data_DF = pd.DataFrame(data_dict)

print(data_series)
print(data_series["range"])
print(series)
print(data_DF["range"])
print(data_DF["range"][:6:2])
print(data_DF.loc[5:9])