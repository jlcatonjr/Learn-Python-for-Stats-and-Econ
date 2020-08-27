#forLoopWithoutIndexer.py
list1 = ["red", "blue", "orange", "black", "white", "golden"]
list2 = []
for x in list1:
    list2.append(x)

print("list1\t", "list2")
k = len(list1)
j = len(list2)

if len(list1) == len(list2):
    for i in range(0, len(list1)):
        print(list1[i], "\t", list2[i])