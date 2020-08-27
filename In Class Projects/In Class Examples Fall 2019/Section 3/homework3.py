#homework3.py
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
    #lists of even length divided by 2 have remainder 0
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
    mode =[key for key in counter_dict if counter_dict[key] == max_count]

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

def covariance(list_obj1, list_obj2, sample = False):
    # determine the mean of each list
    mean1 = mean(list_obj1)
    mean2 = mean(list_obj2)
    # instantiate a variable holding the value of 0; this will be used to 
    # sum the values generated in the for loop below
    cov = 0
    n1 = len(list_obj1)
    n2 = len(list_obj2)
    # check list lengths are equal
    if n1 == n2:
        # sum the product of the diferrence between each observation and the
        # mean for var1 and var2
        for i in range(n1):
            cov += (list_obj1[i] - mean1) * (list_obj2[i] - mean2)
        if sample == False:
            cov = cov / n1
        # account for sample by dividing by one less than number of elements
        # in list
        else:
            cov = cov / (n1 - 1)
        #return covariance
        return cov
    else:
        print("List lengths are not equal")
        print("List1 observations:", n1)
        print("List2 observations:", n2)

def correlation(list_obj1, list_obj2):
    # corrxy = cov(x,y) / (SD(X) * SD(y))
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
    skew = skew / n if not sample else n * skew / ((n - 1) * (n - 2))
    SD_ = SD(list_obj, sample)
    skew = skew / (SD_ ** 3)
    
    return skew
    
def kurtosis(list_obj, sample = False):
    mean_ = mean(list_obj)
    # start calc at 0, then sum all (xi - xmean) ** 4
    kurt = 0
    n = len(list_obj)
    for x in list_obj:
        kurt += (x - mean_) ** 4
    SD_ = SD(list_obj, sample)
    # transform sum(xi - xmean) ** 4 in light of pop or sample...
    kurt = kurt / (n * SD_ ** 4) if not sample else \
        n * (n + 1) * kurt / ((n - 1) * (n - 2) * (SD_ ** 4)) -\
        (3 *(n - 1) ** 2) / ((n - 2) * (n - 3))
    
    return kurt        

print("""
James Caton
ECON 411 / 611
Homework 3
""")

print("""
1. Create a list of random numbers between 0 and 100 whose length is 1000. 
(Hint: import random; search "python random" to learn more about the library.)
""")
def create_rand_list(length, max_rand=100):
# use for loop to iterate code 1000 times, create 1000 random numbers
    lst = []
    for i in range(length):
        #multiply random number between 0 and 1 by 
        rand_num = random.random() * max_rand
        #append rand_num to the end of lst
        lst.append(rand_num) 
    return lst

lst = create_rand_list(length = 100, max_rand = 100)

print("""
SCRIPT:
    
def create_rand_list(length, max_rand=100):
# use for loop to iterate code 1000 times, create 1000 random numbers
    lst = []
    for i in range(length):
        #multiply random number between 0 and 1 by 
        rand_num = random.random() * max_rand
        #append rand_num to the end of lst
        lst.append(rand_num) 
    return lst

lst = create_rand_list(length = 100, max_rand = 100)

RESULT:
"""    )
print(lst)
    
print("""
EXPLANATION:
""")

print("""
3. Create 9 more lists of the same length whose elements are random numbers 
between 0 and 100. Use a nested dictionary to house and identify these lists. 
Keys for the first layer should be the numbers 1 through 10. Lists should be 
stored using a second key as follows: dict_name[index]["list"]. Index 
represents the particular integer key between 1 and 10 as noted above.)
""")
dct = {}
for i in range(10):
    dct[i] = {}
#    lst = create_rand_list(10, 100)
    lst = []
    for j in range(10):
        rand_num = random.random() * 10 ** 2
        lst.append(rand_num)
    dct[i]["list"] = lst
print("""
SCRIPT:
    
dct = {}
for i in range(10):
    dct[i] = {}
#    lst = create_rand_list(10, 100)
    lst = []
    for j in range(10):
        rand_num = random.random() * 10 ** 2
        lst.append(rand_num)
    dct[i]["list"] = lst

RESULT:
""")
print(dct)

print("""
4. Find the variance of each list and store it as follows: 
    dict_name[index]["variance"].""")

for i in range(10):
    dct[i]["variance"] = "VARIANCE OF LIST IN ENTRY I..."
    print(dct[i]["variance"])

