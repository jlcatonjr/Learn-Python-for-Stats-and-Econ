#listFromGenerator.py
# create a generator of length 20 i in range [0,19]
generator = (i for i in range(20))
print(generator)

# use the generator to create a list using list(generator)
list1 = list(generator)
print(list1)

# place teh generator with an "empty" list to create
# a list with values specified by the generator
list2 = [2 * i for i in range(20)]
print(list2)