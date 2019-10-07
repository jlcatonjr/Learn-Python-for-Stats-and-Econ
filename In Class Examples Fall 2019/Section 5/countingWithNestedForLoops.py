#countingWithNestedForLoops.py
import numpy as np

#Example 1
# recall how to count using a for loop:
max_count = 100
for i in range(100):
    print(i)

#Example 2a
# Counting with nested for loops offers an opportunity to think about
# 1. The structure of a number system of different bases
# 2. The structure of multidimensional arrays

# consider counting to 100 in base 10:

count_list = []
base10_count_list = []

# try changing the base to see how the count changes
# the program will count to base ** 2 - 1
# provides interpretable results work for all bases up to 10
base = 3
for i in range(base):
    for j in range(base):
        val = int(str(i) + str(j))
        count_list.append(val)
        #produce equivalent list in base10
        base10_val = i * base + j
        base10_count_list.append(base10_val)
print("\ncount in base", base)
print(count_list)
print("\ncount in base 10:")
print(base10_count_list)

#Example 2b
#imagine that you wanted to count to base ** 3 - 1
count_list = []
base10_count_list = []
# try changing the base to see how the count changes
# the program will count to base ** 3 - 1
# provides interpretable results work for all bases up to 10
for i in range(base):
    for j in range(base):
        for k in range(base):        
            val = int(str(i) + str(j) + str(k))
            count_list.append(val)
            #produce equivalent list in base10
            base10_val = i * base ** 2 + j * base + k
            base10_count_list.append(base10_val)

print("\ncount in base", base)
print(count_list)
print("\ncount in base 10:")
print(base10_count_list)

#Example 3
# We can use the same logic to fill an n X n array with values:
n = base
array = np.zeros((n,n))
for i in range(n):
    for j in range(n):
        array[i][j] = i * n + j
print(array)