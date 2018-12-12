#statsFunctions2.py
def total(list_obj):
    total = 0
    for i in range(len(list_obj)):
        total += list_obj[i]
    return total

def mean(list_obj):
    mean = total(list_obj) / len(list_obj)
    return mean

list1 = [3, 6, 9, 12, 15]
total_list1 = total(list1)
print(total_list1)

mean_list1 = mean(list1)
print("Mean of list1:", mean_list1)

