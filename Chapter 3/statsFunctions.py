#statsFunctions.py
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
    if len(list_obj) %2 != 0:
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


print(mean([1,2,3]))
print(median([1,2,3]))
print(mode([1,2,3,3]))