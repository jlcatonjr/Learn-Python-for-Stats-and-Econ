#removeListElementsPop.py

# define list1 and list2
list1 = ["red", "blue", "orange", "black", "white", "golden"]
list2 = ["nose", "ice", "fire", "cat", "mouse", "dog"]

#identify what is printed in for loop
print("lists before deletion: ")
# use for loop to print lists in parallel
for i in range(len(list1)):
    print(list1[i], "\t", list2[i])

#remove list elements and save them as variables "_res"
list1_res = list1.pop(0)
list2_res = list2.pop(5)

print()
# print lists again as in lines 8-11
print("lists after deletion: ")
for i in range(len(list1)):
    print(list1[i], "\t", list2[i])
print()
print("Res1\tRes2")
#print elements that were removed from list
print(list1_res, "\t", list2_res)