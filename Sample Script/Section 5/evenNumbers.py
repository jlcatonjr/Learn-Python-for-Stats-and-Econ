#evenNumber.py
import numpy as np

even_num = [i for i in range(100) if i % 2 == 0]
print(even_num)

even_nums = np.arange(100)

index = even_nums % 2 == 0
even_nums = even_nums[index]

print(even_nums)
print(index)
