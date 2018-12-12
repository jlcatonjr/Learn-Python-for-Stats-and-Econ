#statsFunctions5.py
def total(list_obj):
    total = 0
    for i in range(len(list_obj)):
        total += list_obj[i]
    return total

def mean(list_obj):
    mean = total(list_obj) / len(list_obj)
    return mean

def median(list_obj):
    median = 0
    if len(list_obj) % 2 != 0:
        index = int((len(list_obj)) / 2)
        median = float(list_obj[index])
    else:
        index1 = int((len(list_obj)) / 2)
        index2 = index1 - 1
        median = (list_obj[index1] + list_obj[index2]) / 2
    return median

def mode(list_obj):
    max_count = 0
    counter_dict = {}
    for value in list_obj:
        counter_dict[value] = 0
    for value in list_obj:
        counter_dict[value] +=1
    count_list = [counter_dict[value] for value in counter_dict]
    max_count = max(count_list)
    ix = [i for i, j in enumerate(count_list) if j == max_count]
    mode = []
    for i in ix:
        mode.append(list_obj[i])
    return mode

def variance(list_obj):
    list_mean = mean(list_obj)
    n = len(list_obj)
    sum_sq_diff = 0
    for x in list_obj:
        sum_sq_diff += (x - list_mean) ** 2
    variance = sum_sq_diff / n
    return variance

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

mode_list1 = mode(list1)
mode_list2 = mode(list2)
print("Mode of list1:", mode_list1)
print("Mode of list2:", mode_list2)

variance_list1 = variance(list1)
variance_list2 = variance(list2)
print("Variance of list1:", variance_list1)
print("Variance of list2:", variance_list2)