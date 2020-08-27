#statsFunctions11.py
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
    count_list = list(counter_dict.values())
    max_count = max(count_list)
    keys = [key for key in counter_dict if counter_dict[key] == max_count]
    mode = []
    for key in keys:
        mode.append(key)
    return mode

def variance(list_obj, sample = False):
    list_mean = mean(list_obj)
    n = len(list_obj)
    sum_sq_diff = 0
    for x in list_obj:
        sum_sq_diff += (x - list_mean) ** 2
    if sample == False:
        variance = sum_sq_diff / n
    else:
        variance = sum_sq_diff / ( n-1)
    return variance

def SD(list_obj, sample = False):
    if sample == False:
        SD = variance(list_obj) ** 1/2
    else:
        SD = variance(list_obj,sample = True) ** (1/2)
    return SD

def covariance(list_obj1, list_obj2, sample = False):
    mean1 = mean(list_obj1)
    mean2 = mean(list_obj2)
    cov = 0
    n1 = len(list_obj1)
    n2= len(list_obj2)
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
    for x in list_obj:
        skew += (x - mean_) ** 3

    skew = skew / n if not sample else skew / (n - 1)
    SD_ = SD(list_obj, sample) 
    skew = skew / (SD_ ** 3)
    return skew

def kurtosis(list_obj, sample = False):
    mean_ = mean(list_obj)
    kurt = 0
    n = len(list_obj)
    for x in list_obj:
        kurt += (x - mean_) ** 4
    SD_ = SD(list_obj, sample)
    kurt = kurt / n if not sample else kurt / (n - 1)
    kurt = kurt / (SD_ ** 4)
    
    return kurt
    
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

kurt_list1 = kurtosis(list1)
kurt_list2 = kurtosis(list2)
print("Kurtosis of list1:", kurt_list1)
print("Kurtosis of list2:", kurt_list2)

kurt_list1_sample = kurtosis(list1, True)
kurt_list2_sample = kurtosis(list2, True)
print("Kurtosis of list1 as sample:", kurt_list1_sample)
print("Kurtosis of list2 as sample:", kurt_list2_sample)