#statsFunctions10.py
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

def mode(list_obj):
    max_count = 0
    counter_dict = {}
    for value in list_obj:
        counter_dict[value] = 0
    for value in list_obj:
        counter_dict[value] +=1
    count_list = list(counter_dict.values())
    max_count = max(count_list)
    mode = [key for key in counter_dict if counter_dict[key] == max_count]

    return mode

def variance(list_obj, sample = False):
    list_mean = mean(list_obj)
    n = len(list_obj)
    sum_sq_diff = 0
    for val in list_obj:
        sum_sq_diff += (val - list_mean) ** 2
    if sample == False:
        variance = sum_sq_diff / n
    else:
        variance = sum_sq_diff / (n - 1)
    return variance

def SD(list_obj, sample = False):
    SD = variance(list_obj, sample) ** (1/2)
    return SD

def covariance(list_obj1, list_obj2, sample = False):
    mean1 = mean(list_obj1)
    mean2 = mean(list_obj2)
    cov = 0
    n1 = len(list_obj1)
    n2 = len(list_obj2)
    if n1 == n2:
        for i in range(n1):
            cov += (list_obj1[i] - mean1) * (list_obj2[i] - mean2)
        if sample == False:
            cov = cov / n1
        else:
            cov = cov / (n1 - 1)
        return cov
    else:
        print("List observations not equal")
        print("List1 observations:", n1)
        print("List2 observations:", n2)
        quit()

def correlation(list_obj1, list_obj2):
    cov = covariance(list_obj1, list_obj2)
    SD1 = SD(list_obj1)
    SD2 = SD(list_obj2)
    corr = cov / (SD1 * SD2)
    return corr
        
def skewness(list_obj, sample = False):
    mean_ = mean(list_obj)
    skew = 0
    n = len(list_obj)
    for val in list_obj:
        skew += (val - mean_) ** 3

    skew = skew / n if not sample else skew / (n - 1)
    SD_ = SD(list_obj, sample) 
    skew = skew / (SD_ ** 3)
    return skew
    
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

SD_list1 = SD(list1)
SD_list2 = SD(list2)
print("Standard deviation of list1:", SD_list1)
print("Standard deviation of list2:", SD_list2)

sample_SD_list1 = SD(list1, sample = True)
sample_SD_list2 = SD(list2, sample = True)
print("Standard deviation of list1 as sample:", sample_SD_list1)
print("Standard deviation of list2 as sample:", sample_SD_list2)

list2 = [1,1,1,1,5]
cov_pop_list1_list2 = covariance(list1, list2, sample = False)
cov_sam_list1_list2 = covariance(list1, list2, sample = True)
print("Covariance of population:", cov_pop_list1_list2)
print("Covariance of sample:", cov_sam_list1_list2)

corr_list1_list2 = correlation(list1, list2)
print("Correlation of list1 and list2:", corr_list1_list2)

skew_list1 = skewness(list1)
skew_list2 = skewness(list2)
print("Skewness of list1:", skew_list1)
print("Skewness of list2:", skew_list2)

skew_list1_sample = skewness(list1, True)
skew_list2_sample = skewness(list2, True)
print("Skewness of list1 as sample:", skew_list1_sample)
print("Skewness of list2 as sample:", skew_list2_sample)