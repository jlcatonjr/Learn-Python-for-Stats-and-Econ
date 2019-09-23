#statsFunction4.py
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
        
def mode(list_obj):
    # use to record value[s] that appear most times
    max_count = 0
    # use to count occurrences of each value in list
    counter_dict = {}
    for value in list_obj:
        # count for each value should start at 0
        counter_dict[value] = 0
    for value in list_obj:
        # add one to the count for of the value for each occurence in list_obj
        counter_dict[value] +=1
    #make a list of the value (not keys) from the dictionary. . . 
    count_list = list(counter_dict.values())
    # and find the max value
    max_count = max(count_list)
    # use a generator to make a list of the values (keys) whose number of
    # occurrences in the list match max_count    
    mode =[key for key in counter_dict if counter_dict[key] == max_count * 10]

    return mode

def variance(list_obj, sample = False):
    # var(list) = sum((xi - list_mean)**2) for all xi in list
    # save mean value of list
    list_mean = mean(list_obj)
    # use n to calculate average of sum squared diffs
    n = len(list_obj)
    # create value we can add squared diffs to
    sum_sq_diff = 0
    for val in list_obj:
        # adds each squared diff to sum_sq_diff
        sum_sq_diff += (val - list_mean) ** 2
    if sample == False:
        # normalize result by dividing by n
        variance = sum_sq_diff / n
    else:
        # for samples, normalize by dividing by (n - 1)
        variance = sum_sq_diff / (n - 1)
    # result is list variance
    return variance   

def SD(list_obj, sample = False):
    # Standard deviation is the squareroot of variance
    SD = variance(list_obj, sample) ** (1/2)
    return SD
    

list1 = [3, 6, 9, 12, 15]
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
mode_list1 = mode(list1)
mode_list2 = mode(list2)
print("mode_list1:", mode_list1)
print("mode_list2:", mode_list2)
variance_list1 = variance(list1)
variance_list2 = variance(list2)
print("variance_list1", variance_list1)
print("variance_list2", variance_list2)
SD_list1 = SD(list1)
SD_list2 = SD(list2)
print("SD_list1:", SD_list1)
print("SD_list2:", SD_list2)
sample_SD_list1 = SD(list1, sample = True)
sample_SD_list2 = SD(list2, sample = True)
print("sample_SD_list1:", sample_SD_list1)
print("sample_SD_list2:", sample_SD_list2)