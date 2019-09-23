#addListElements.py
list1 = [5, 4, 9, 10, 3, 5]
list2 = [6, 3, 2, 1, 5, 3]
print("list1 elements:", list1[0], list1[1], list1[2], list1[3], list1[4], 
      list1[5])
print("list2 elements:", list2[0], list2[1], list2[2], list2[3], list2[4],
      list2[5])

list3 = []
j = len(list1)
k = len(list2)
# compare of lists
if j == k:
    #count by 2s from 0 to len(list1 - 1)
    for i in range(0, j, 2):
        list3.append(list1[i] + list2[i])
# if list1 and list2 not same length, note error 
else:
    print("Lists are not the same length, cannot perform element-wise operations.")
print("list3:", list3)

# print list elements with for-loop
print("list1 elements: ", end="")
for i in range(j):
    print(str(list1[i]), end = " ")
    