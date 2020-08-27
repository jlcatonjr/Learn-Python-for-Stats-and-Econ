#copyListsElement.py

list1 = [5, 4, 9, 10, 3, 5]
list2 = [6, 3, 2, 1, 5, 3]
print("list1 elements:", list1[0], list1[1], list1[2], list1[3], list1[4],
      list1[5])
print("list2 elements:", list2[0], list2[1], list2[2], list2[3], list2[4],
      list2[5])

# the ith values in list3 are the some of the ith values from list1 and list2
list3 = []
list3.append(list1[0])
list3.append(list1[1])
list3.append(list1[2])
list3.append(list1[3])
list3.append(list1[4])
list3.append(list1[5])
print("list3:", list3)

list4 = []
list4.append(list1[0] + list2[0])
list4.append(list1[1] + list2[1])
list4.append(list1[2] + list2[2])
list4.append(list1[3] + list2[3])
list4.append(list1[4] + list2[4])
list4.append(list1[5] + list2[5])
print("list4:", list4)