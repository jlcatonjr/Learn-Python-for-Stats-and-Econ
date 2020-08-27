#sortingError.py
list1 = [5, 4, 9, 10, 3, 5]
list2 = ["red", "blue", "orange", "black", "white", "golden"]
list3 = list1 + list2

print("list1:", list1)
print("list2:", list2)
print("list3:", list3)

sorted_list1 = sorted(list1)
sorted_list2 = sorted(list2)

print("sortedList1:", sorted_list1)
print("sortedList2:", sorted_list2)
try:
    sorted_list3 = sorted(list3)
    print("sortedList3:", sorted_list3)
except:
    print("TypeError: unorderable types: str() < int()) "
         "ignoring error")
print("Execution complete!")