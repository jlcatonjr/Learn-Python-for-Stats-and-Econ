#evenNumbers.py
import numpy as np 

even_nums = [i for i in range(100) if i % 2 == 0]
print(even_nums)

even_nums = np.arange(100)
print(even_nums)
index_array = even_nums % 2 == 0
print(index_array)
even_nums = even_nums[index_array]
print(even_nums)

even_nums_types = [type(val) for val in even_nums]
print(even_nums_types)