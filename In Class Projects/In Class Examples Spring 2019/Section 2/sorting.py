#sorting.py
list1 = [5, 4, 9, 10, 3, 5]
list2 = ["red", "blue", "orange", "black", "white", "golden"]

print("list1:", list1)
print("list2:", list2)

sorted_list1 = sorted(list1)
sorted_list2 = sorted(list2)

print("sorted_list1:", sorted_list1)
print("sorted_list2:", sorted_list2)

set_list1 = set(list1)
print("reduced_set:", set_list1)
reduced_list1 = []
for key in set_list1:
    reduced_list1.append(key)
print("reduced_list1:", reduced_list1)
