#removeListElements.py
list1 = ["red", "blue", "orange", "black", "white", "golden"]
list2 = ["nose", "ice", "fire", "cat", "mouse", "dog"]
print("lists before deletion: ")
for i in range(len(list1)):
    print(list1[i],"\t", list2[i])
    
list1.remove("red")
list2.remove("dog")

print()
print("lists after deletion: ")
for i in range(len(list1)):
    print(list1[i], "\t",list2[i])     