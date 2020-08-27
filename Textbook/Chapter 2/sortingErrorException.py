#sortingErrorException.py
list1 = [5, 4, 9, 10, 3, 5]
list2 = ["red", "blue", "orange", "black", "white", "golden"]
list3 = list1 + list2

print("list1:", list1)
print("list2:", list2)
print("list3:", list3)

sortedList1 = sorted(list1)
sortedList2 = sorted(list2)
try:
    sortedList3 = sorted(list3)
except:
    sortedList3 = "Lists with 'str' *and* 'int' cannot be sorted"

print("sortedList1:", sortedList1)
print("sortedList2:", sortedList2)
print("sortedList3:", sortedList3)
