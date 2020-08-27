#listFromGenerator.py

generator = (i for i in range(20))
print(generator)

list1 = list(generator)
print(list1)

list2 = [2 * i for i in range(20)]
print(list2)