#numpyzeros.py
import numpy as np

array = np.zeros((3,3))
empty_array = np.empty((5,3))
print(array)
print(empty_array)

array[0][2] = 9
array[1][0] = 7
array[2][2] = 3
print(array)