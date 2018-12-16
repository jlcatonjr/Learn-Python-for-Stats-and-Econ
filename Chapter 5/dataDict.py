import numpy as np

dataDict = {"1 to 10":np.arange(10),
            "ones":np.ones(10),
            "zeros":np.zeros(10)}
print(dataDict)
print([dataDict[key] for key in dataDict])
print([key + " " + str(dataDict[key])  for key in dataDict])
print([key + " " + str(dataDict[key][5:10])  for key in dataDict])
#
#dataDict["1 to 100 + Ones"] = dataDict["1 to 10"] + dataDict["ones"]
#print(dataDict["1 to 100 + Ones"])
