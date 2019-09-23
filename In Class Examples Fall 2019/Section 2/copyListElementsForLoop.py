#copyListsElement.py
# creating lists with integers as elements
list1 = [5, 4, 9, 10, 3, 5]
list2 = [6, 3, 2, 1, 5, 4]
# record length of the list to appropriately calibrate the for loop
len_list1 = len(list1)
len_list2 = len(list2)
print("list1 elements:", end=" ")
# call a value i for every i in index of list1
for i in range(len_list1):
    # for each i in list 1, print i and add space at end
    print(list1[i], end=" ")
#add space after line where list1 elements are printed
print()
# repeat same process as in above few lines
print("list2 elements:", end = " ")
for i in range(len_list2):
    print(list2[i], end=" ")
# print a new line in the console
print()    
# the ith values in list3 are the some of the ith values from list1 and list2
list3 = []
# copying elements from list1 to a new list, list3
for i in range(len_list1):
    # append the ith element from list 1 to the end of list3
    # as it has so far been constructed
    list3.append(list1[i])
    # print list3 constructed so far with index i
    print(i, list3)

print("list3:", list3)

list4 = []
# make sure that lists are the same length before calling each index
if len_list1 == len_list2:
    # append the sum of the ith elements from list1 and list2 to list4
    for i in range(len_list1):
        list4.append(list1[i] + list2[i])
        print(i, list4)
#if lists are not same length, print error statement in console
else:
    print("WARNING!!!!!!!")
    print("list1 has", len_list1, "elements")
    print("list2 has", len_list2, "elements")
    print("len_list1 != len_list2")
    
print("list4:", list4)