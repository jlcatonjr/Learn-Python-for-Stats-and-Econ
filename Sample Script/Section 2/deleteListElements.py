#deleteListElements.py

colors = ["red", "blue", "orange", "black", "white", "golden"]
list2 = ["nose", "ice", "fire", "cat", "mouse", "dog"]
len_colors = len(colors)
len_list2 = len(list2)

if len_colors == len_list2:
    for i in range(len_colors):
        print(colors[i], "\t", list2[i])
#print("\n")
print()
del colors[0]
del list2[5]

len_colors = len(colors)
len_list2 = len(list2)

print("lists after deletion: ")
if len_colors == len_list2:
    for i in range(len_colors):
        print(colors[i],"\t", list2[i])
