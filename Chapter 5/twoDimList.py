#twoDimensionalListAndNumpyArray.py
import numpy as np

twoDimList = [[1,2,3,4],[2,3,4,5]]
print(twoDimList)
twoDimArray = np.array(twoDimList)
print(twoDimArray)

for i in range(len(twoDimList)):
    print(twoDimList[i])
    print(twoDimArray[i])
    for j in range(len(twoDimList[i])):
        print(twoDimList[i][j])
        print(twoDimArray[i][j])