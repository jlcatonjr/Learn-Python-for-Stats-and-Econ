#twoDimensionalListAndNumpyArray.py
import numpy as np
two_dim_list = [[1,2,3,4],[2,3,4,5]]
print(two_dim_list)
two_dim_array = np.array(two_dim_list)
print(two_dim_array)

for i in range(len(two_dim_list)):
    print(two_dim_list[i])
    print(two_dim_array[i])
    for j in range(len(two_dim_list[i])):
        print(two_dim_list[i][j])
        print(two_dim_array[i][j]) 