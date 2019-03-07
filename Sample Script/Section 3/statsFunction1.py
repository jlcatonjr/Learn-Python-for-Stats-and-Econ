#statsFunction1.py

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
    # lists of even length divided by 2 have remainder of 0
    if n % 2 != 0:
        #list is odd
        middle_num = int((n - 1) / 2)
        median = list_obj[middle_num]
    else:
        middle_num2 = int(n/2)
        middle_num1 = middle_num2 - 1
        # pass slice with two middle values to mean()
        median = mean(list_obj[middle_num1:middle_num2 + 1])
    
    return median

def mode(list_obj):
    max_count = 0
    counter_dict = {}
    for value in list_obj:
        counter_dict[value] = 0
    for value in list_obj:
        counter_dict[value] += 1
    count_list = list(counter_dict.values())
    max_count = max(count_list)
    mode = [key for key in counter_dict if counter_dict[key] == max_count]
    
    return mode 

def variance(list_obj, sample = False):
    """ Step 1 """
    list_mean = mean(list_obj)
    n = len(list_obj)
    """ Step 2 """
    sum_sq_diff = 0
    for val in list_obj:
        sum_sq_diff += (val - list_mean) ** 2
    if sample == False:
        list_variance = sum_sq_diff / n
    if sample == True:
        list_variance = sum_sq_diff / (n - 1)
    return list_variance

def SD(list_obj, sample = False):
    list_variance = variance(list_obj, sample)
    list_SD = list_variance ** (1/2)
    
    return list_SD

def covariance(list1, list2, sample = False):
    """ 
    1. Check lengths of lists are the same
    2. Calculate the means
    3. Use a for loop to sum product of the differences for each observation
        from both lists
    4. Divide by the number of observations
    """
    len_list1 = len(list1)
    len_list2 = len(list2)
    if len_list1 == len_list2:
        mean_list1 = mean(list1)
        mean_list2 = mean(list2)
        sum_of_diff_prods = 0
        for i in range(len_list1):
            diff_list1 = list1[i] - mean_list1
            diff_list2 = list2[i] - mean_list2
            sum_of_diff_prods += diff_list1 * diff_list2
        if sample == False:    
            cov = sum_of_diff_prods / len_list1
        if sample:
            cov = sum_of_diff_prods / (len_list1 - 1)
        return cov
    
    print("List lengths not equal")
    print("List1 observations:", len_list1)
    print("List2 observations:", len_list2)

    return None
    
def correlation(list1, list2):
    cov = covariance(list1, list2)
    SD1 = SD(list1)
    SD2 = SD(list2)
    corr = cov / (SD1 * SD2)
    return corr
            
def skewness(list_obj, sample = False):  
    mean_ = mean(list_obj)  
    skew = 0  
    n = len(list_obj)  
    for x in list_obj:  
        skew += (x - mean_) ** 3  
  
        skew = skew / n if not sample else  n * skew / ((n - 1) * (n - 2))
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
    kurt = kurt / n if not sample else \
    n * (n+1) kurt / ((n - 1)(n – 2)) – (3(n – 1) ** 2) / ((n – 2) * (n – 3))
    kurt = kurt / (SD_ ** 4)  
    return kurt  


list1 = [3, 6, 9, 12, 15]
total_list1 = total(list1)
print("Total of list1:", total_list1)
mean_list1 = mean(list1)
print("Mean of list1:", mean_list1)
median_list1 = median(list1)
print("Median of list1:", median_list1)
list2 = [1,1,1,1,1,5]
median_list2 = median(list2)
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
print("Standard Deviation of list1:", SD_list1)
print("Standard Deviation of list2:", SD_list2)

# Pass lists as sample to variance() and SD()
sample_variance_list1 = variance(list1, sample=True)
sample_variance_list2 = variance(list2, sample=True)
print("Variance of list1 as sample:", sample_variance_list1)
print("Variance of list2 as sample:", sample_variance_list2)
sample_SD_list1 = SD(list1, sample = True)
sample_SD_list2 = SD(list2, sample = True)
print("Standard Deviation of list1 as sample:", sample_SD_list1)
print("Standard Deviation of list2 as sample:", sample_SD_list2)
list1.insert(0,3)
cov_pop_list1_list2 = covariance(list1, list2, sample = False)
cov_sample_list1_list2 = covariance(list1, list2, sample = True)
print("Covariance of population:", cov_pop_list1_list2)
print("Covariance of sample:", cov_sample_list1_list2)
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
