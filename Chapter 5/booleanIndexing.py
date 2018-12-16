#booleanIndexing.py
import random
import numpy as np

rand_list = [random.random() * 10 for i in range(7)]
print("rand_list values:", rand_list)
rand_list = [i for i in rand_list if i > 3]
print("rand_list values > 3:", rand_list)

rand_array = np.random.randn(7) * 10
print("rand_array:", rand_array)
print("rand_array > 3:", rand_array[rand_array > 3])