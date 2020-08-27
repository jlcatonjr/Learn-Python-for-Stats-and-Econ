#addListElements3.py
list1 = [5, 4, 9, 10, 3, 5]
list2 = [6, 3, 2, 1, 5]
print("list1 elements:", list1[0], list1[1], list1[2], list1[3], list1[4],
      list1[5])
if len(list2) == 6:
    print("list2 elements:", list2[0], list2[1], list2[2], list2[3], list2[4],
          list2[5])

list3 = []
j=len(list1)
# if statement checks that the length of each list is equal
if len(list1) == len(list2):
    for i in range(j):
        # .insert places the element at a particular index in list
        list3.insert(i, list1[i] + list2[i])
else:
    # "\" tells the program to move to the next len whe followed by a return
    print("Lists are not the same length, cannot perform element-wise \
operations.")

print("list3:", list3)