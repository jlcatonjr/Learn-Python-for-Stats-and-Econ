#evenNumbers.py
import numpy as np 

even_nums = [i for i in range(100) if i % 2 == 0]
print(even_nums)

even_nums = np.arange(100)
even_nums = even_nums[even_nums % 2 == 0]
print(even_nums)