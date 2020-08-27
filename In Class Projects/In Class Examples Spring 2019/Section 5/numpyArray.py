#numpyArray.py
import numpy as np

lst = [1.,2.,3.,4.,5.]
np_array = np.array(lst)
print("list:", lst)
print("np_array:", np_array)
print(np_array.dtype)
print("list dtype", type(lst))
print("np_array dtype", type(np_array))