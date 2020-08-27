#twoDimensionalListAndNumpyArray.py
import numpy as np

two_dim_list = [[1,2,3,5], [2,3,4,5], [1,5,6,3],
                [2,3,5,7], [3,1,5,6], [5,6,3,3]]
#print("len(two_dim_list) =", len(two_dim_list))
#print(two_dim_list)

for i in range(len(two_dim_list)):
    sub_list_i = two_dim_list[i]
    for j in range(len(sub_list_i)):
        print(i, j, sub_list_i[j])
two_dim_array = np.array(two_dim_list)
print(two_dim_array)
    