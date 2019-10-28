import pandas as pd
data = pd.read_excel("index2017_data.xls", index_col = [1])
#data = data[["World Rank", "2017 Score", "Property Rights", 
#             "Judical Effectiveness"]]

for i in data.values:
    print(i)
