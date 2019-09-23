#statsFunctions3.py
def total(list_obj):
    total = 0
    n = len(list_obj)
    for i in range(n):
        total += list_obj[i]
    return total

def mean(list_obj):
    n = len(list_obj)
    mean = total(list_obj) / n
    return mean

def median(list_obj):
    n = len(list_obj)
    if n % 2 != 0:
        middle_num = int((n - 1) / 2)
        median = list_obj[middle_num]
    else:
        upper_middle_num = int(n / 2) 
        lower_middle_num = upper_middle_num - 1
        median = mean(list_obj[lower_middle_num:upper_middle_num + 1])
    
    return median

list1 = [3, 6, 9, 12, 15]
total_list1 = total(list1)
print(total_list1)

mean_list1 = mean(list1)
print("Mean of list1:", mean_list1)

list2 = [1, 1, 1, 1, 1, 5]
median_list1 = median(list1)
median_list2 = median(list2)
print("Median of list1:", median_list1)
print("Median of list2:", median_list2)