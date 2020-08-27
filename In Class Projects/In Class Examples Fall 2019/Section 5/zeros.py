#zeros.py
import numpy as np

array = np.zeros((3,3))
print(array)

array[0][2] = 9
array[1][0] = 7
array[2][2] = 3

print(array)

""" 
make an array using a for loop that prints as:

[[0. 1. 2.]
 [0. 1. 2.]
 [0. 1. 2.]]
"""

for i in range(len(array)):
#    print(i, array[i])
    len_array_i = len(array[i])
    for j in range(len_array_i):               
        array[i][j] = 3 * i + j
        print(i, j, array[i][j])
    
print(array)
    



for i in range(10):
    for j in range(10):
        val = i * 10 + j
        print(val)
    
    
    
    
    
    
    