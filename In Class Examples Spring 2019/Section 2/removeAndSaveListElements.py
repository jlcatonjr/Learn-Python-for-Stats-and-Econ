#removeAndSaveListElements.py

list1 = ["red", "blue", "orange", "black", "white", "golden"]
list2 = ["nose", "ice", "fire", "cat", "mouse", "dog"]
print("lists before deletion: ")
len_list1 = len(list1)
len_list2 = len(list2)

if len_list1 == len_list2:
    for i in range(len_list1):
        print(list1[i], "\t", list2[i])
#print("\n")
print()
list1_res = list1[0]
list2_res = list2[5]
list1.remove(list1_res)
list2.remove(list2_res)

len_list1 = len(list1)
len_list2 = len(list2)

print("lists after deletion: ")
if len_list1 == len_list2:
    for i in range(len_list1):
        print(list1[i],"\t", list2[i])

print()
print("Residual 1\tResidual 2")
print(list1_res + "\t\t" + list2_res)