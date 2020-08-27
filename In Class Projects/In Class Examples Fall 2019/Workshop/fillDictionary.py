import random
import this
dct = {}
for i in range(10):
    lst = []
    for j in range(10):
        lst.append(round(random.random() * 100, 2))
#    dct[i]...
#
dct2 = {}
keys = ["I", "think", "that", "the", "keys", "should", "be", "more", "interesting"]
for i in range(10):
#    lst = []
#    for j in range(10):
#        num = round(random.random() * 100, 2)
#        lst.append(num)
    dct2[i] = [round(random.random() * 100, 2) for j in range(10)]
print(dct2)
    