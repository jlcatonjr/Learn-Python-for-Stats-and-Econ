import pandas as pd


maxExp = 10
lists = {}
for j in range(1,maxExp):
    if j == 1:
        lists["i"] = []
    else:
        lists["i^"+str(j)] = []

for i in range(1,21):
    for j in range(1,maxExp):
        if j == 1:
            lists["i"].append(i ** j)
        else:
            lists["i^" + str(j)].append(i**j)
            
dataFrame = pd.DataFrame(lists)
print(dataFrame)
dataFrame.to_csv("numbers.csv")
    