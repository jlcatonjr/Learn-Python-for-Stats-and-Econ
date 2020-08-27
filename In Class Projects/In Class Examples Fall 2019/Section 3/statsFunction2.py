#statsFunction2.py
def total(list_obj):
    # create variable total; value should
    # be 0 since each number in the list
    # is added to total
    total = 0
    # n is length of object
    n = len(list_obj)
    # n used to call each element in list using for loop
    for i in range(n):
        # add value in list to total
        total += list_obj[i]
    #return the sum of values in list ot be saved as variable
    return total

def mean(list_obj):
    n = len(list_obj)
    mean = total(list_obj) / n
    return mean    

list1 = [3, 6, 9, 12, 15]
list2 = [i ** 2 for i in range(3,8)]
total_list1 = total(list1)
total_list2 = total(list2)
print("total_list1:", total_list1)
print("total_list2:", total_list2)

mean_list1 = mean(list1)
mean_list2 = mean(list2)
print("mean_list1:", mean_list1)
print("mean_list2:", mean_list2)


