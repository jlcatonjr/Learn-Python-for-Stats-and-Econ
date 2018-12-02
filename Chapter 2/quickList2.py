#quickList3.py
list1 = list(range(0,11))
list2 = []
list3 = []
for i in range(len(list1)):
    list2.append(list1[i] ** 2)
    list3.append(list1[i] **2 + list1[i] * 50 - 100)
    print(i, "\tlist1:", list1[i], "\tlist2:", list2[i], "\tlist3:", list3[i])