#statsFunction1.py
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

list1 = [3, 6, 9, 12, 15]
list2 = [3154231,4321,432543]
total_list1 = total(list1)
total_list2 = total(list2)
print("total_list1:", total_list1)
print("total_list2:", total_list2)