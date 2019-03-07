#zerosOnesAndLike.py  
import numpy as np
  
list_of_lists = [[1,2,3],[4,5,6],[7,8,9]]  
array_of_arrays = np.array(list_of_lists)  
zeros_like_array = np.zeros_like(list_of_lists)  
ones_like_array = np.ones_like(list_of_lists)  
empty_like_array = np.empty_like(list_of_lists)  

print("list_of_lists:\n", list_of_lists)  
print("array_of_arrays:\n", array_of_arrays)  	
print("zeros_like_array:\n", zeros_like_array)  
print("ones_like_array:\n", ones_like_array)  
print("empty_like_array:\n", empty_like_array)  