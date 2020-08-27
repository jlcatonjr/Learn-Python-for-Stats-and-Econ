#statsFunctions1.py
def total(list_obj):
    total = 0
    n = len(list_obj)
    for i in range(n):
        total += list_obj[i]
    return total

list1 = [3, 6, 9, 12, 15]
total_list1 = total(list1)
print(total_list1)