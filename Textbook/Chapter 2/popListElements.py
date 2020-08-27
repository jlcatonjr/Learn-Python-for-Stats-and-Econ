#removeListElements.py

list1 = ["red", "blue", "orange", "black", "white", "golden"]
list2 = ["nose", "ice", "fire", "cat", "mouse", "dog"]
print("lists before deletion: ")
for i in range(len(list1)):
    print(list1[i],"\t", list2[i])
    
list1_res = list1.pop(0)
list2_res = list2.pop(5)

print()
print("lists after deletion: ")
for i in range(len(list1)):
    print(list1[i], "\t",list2[i])     
    
print()
print("Res1", "\tRes2")
print(list1_res, "\t" + (list2_res))