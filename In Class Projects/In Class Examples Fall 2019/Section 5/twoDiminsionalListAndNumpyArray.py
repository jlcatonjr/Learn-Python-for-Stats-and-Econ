#twoDimensionalListAndNumpyArray.py
import numpy as np

two_dim_list = [[1,2,3,5], [2,3,4,5], [1,5,6,3,4,5,76,7,98,.9],
                [2,3,5,7], [3,1,5,6], [5,6,3,3]]
two_dim_array = np.array(two_dim_list)
print(two_dim_array)


# i indicates index of outer list
# j indicates element in list i
#print("i","j", "val")
for i in range(len(two_dim_list)):
    sub_list_i = two_dim_list[i]
    sub_array_i = two_dim_array[i]
    print(i, sub_list_i)
    print(i, sub_array_i)
    len_sub_list_i = len(sub_list_i)
    print("len(sub_list_i):", len_sub_list_i)
    for j in range(len_sub_list_i):
        print(i, j, sub_list_i[j])
        print(i, j, sub_array_i[j])