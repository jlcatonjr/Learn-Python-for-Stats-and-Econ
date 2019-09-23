#statsFunction3.py
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

def median(list_obj):
    n = len(list_obj)
    list_obj = sorted(list_obj)
    print(list_obj)
    #l ists of even length divided by 2 have remainder 0
    if n % 2 != 0:
        #list length is odd
        middle_index = int((n - 1) / 2)
        median = list_obj[middle_index]
    else:
        upper_middle_index = int(n/2)
        lower_middle_index = upper_middle_index - 1
        # pass slice with two middle values to mean()
        median = mean(list_obj[lower_middle_index:upper_middle_index + 1])
    
    return median
        
list1 = [3, 6, 9, 12, 15]
#list2 = [i ** 2 for i in range(3,9)]
list2 = [3,7,12,5,7,98]
total_list1 = total(list1)
total_list2 = total(list2)
print("total_list1:", total_list1)
print("total_list2:", total_list2)
mean_list1 = mean(list1)
mean_list2 = mean(list2)
print("mean_list1:", mean_list1)
print("mean_list2:", mean_list2)
median_list1 = median(list1)
median_list2 = median(list2)
print("median_list1:", median_list1)
print("median_list2:", median_list2)

