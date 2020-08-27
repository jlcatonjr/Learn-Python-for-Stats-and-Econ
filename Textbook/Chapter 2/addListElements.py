#addListElements.py
list1 = [5, 4, 9, 10, 3, 5]
list2 = [6, 3, 2, 1, 5, 3]

print("list1 elements:", list1[0], list1[1], list1[2], list1[3], list1[4])
print("list2 elements:", list2[0], list2[1], list2[2], list2[3], list2[4])

list3 = []
j = len(list1)
for i in range(j):
    list3.append(list1[i] + list2[i])
    
print("list3:", list3)
