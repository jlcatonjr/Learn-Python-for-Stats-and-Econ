#dataDict.py
import numpy as np
import pandas as pd

data_dict = {"1 to 10": np.arange(10),
             "ones":np.ones(10),
             "zeroes": np.zeros(10)}

data_DF = pd.DataFrame(data_dict)

print(data_dict)
print([key + str(data_dict[key][5:]) for key in data_dict])
print(data_DF)