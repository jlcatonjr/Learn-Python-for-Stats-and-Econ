#stats.py
class stats():
    def __init__(self):
        print("You created an instance of stats()")
        
    def total(self, list_obj):
        total = 0
        n = len(list_obj)
        for i in range(n):
            total += list_obj[i]
        return total
    
    def mean(self, list_obj):
        n = len(list_obj)
        mean_ = self.total(list_obj) / n
        return mean_ 
    
    def median(self, list_obj):
        n = len(list_obj)
        list_obj = sorted(list_obj)
        # lists of even length divided by 2 have a remainder
        if n % 2 != 0:
            # list length is odd
            middle_index = int((n - 1) / 2)
            median_ = list_obj[middle_index]
        else:
            upper_middle_index = int(n / 2)
            lower_middle_index = upper_middle_index - 1
            # pass slice with two middle values to self.mean()
            median_ = self.mean(list_obj[lower_middle_index : upper_middle_index + 1])
        
        return median_
    
    def mode(self, list_obj):
        # use to record value(s) that appear most times
        max_count = 0
        # use to count occurrences of each value in list
        counter_dict = {}
        for value in list_obj:
            # count for each value should start at 0
            counter_dict[value] = 0
        for value in list_obj:
            # add on to the count of the value for each occurrence in list_obj
            counter_dict[value] += 1
        # make a list of the value (not keys) from the dictionary
        count_list = list(counter_dict.values())
        # and find the max value
        max_count = max(count_list)
        # use a generator to make a list of the values (keys) whose number of 
        # occurences in the list match max_count
        mode_ = [key for key in counter_dict if counter_dict[key] == max_count]

        return mode_
    
    def variance(self, list_obj, sample = False):

        # popvar(list) = sum((xi - list_mean)**2) / n for all xi in list
        # save mean value of list
        list_mean = self.mean(list_obj)
        # use n to calculate average of sum squared diffs
        n = len(list_obj)
        # create value we can add squared diffs to
        sum_sq_diff = 0
        for val in list_obj:
            # adds each squared diff to sum_sq_diff
            sum_sq_diff += (val - list_mean) ** 2
        if sample == False:
            # normalize result by dividing by n
            variance_ = sum_sq_diff / n
        else:
            # for samples, normalize by dividing by (n-1)
            variance_ = sum_sq_diff / (n - 1)

        return variance_
    
    def SD(self, list_obj, sample = False):
        SD_ = self.variance(list_obj, sample) ** (1/2)
        
        return SD_
    
    def covariance(self, list_obj1, list_obj2, sample = False):
        # determine the mean of each list
        mean1 = self.mean(list_obj1)
        mean2 = self.mean(list_obj2)
        # instantiate a variable holding the value of 0; this will be used to 
        # sum the values generated in the for loop below
        cov = 0
        n1 = len(list_obj1)
        n2 = len(list_obj2)
        # check list lengths are equal
        if n1 == n2:
            n = n1
            # sum the product of the differences
            for i in range(n1):
                cov += (list_obj1[i] - mean1) * (list_obj2[i] - mean2)
            if sample == False:
                cov = cov / n
            # account for sample by dividing by one less than number of elements in list
            else:
                cov = cov / (n - 1)
            # return covariance
            return cov
        else:
            print("List lengths are not equal")
            print("List1:", n1)
            print("List2:", n2)

    def correlation(self, list_obj1, list_obj2):
        # corr(x,y) = cov(x, y) / (SD(x) * SD(y))
        cov = self.covariance(list_obj1, list_obj2)
        SD1 = self.SD(list_obj1)
        SD2 = self.SD(list_obj2)
        corr = cov / (SD1 * SD2)
        
        return corr
    
    def skewness(self, list_obj, sample = False):
        mean_ = self.mean(list_obj)
        SD_ = self.SD(list_obj, sample)
        skew = 0
        n = len(list_obj)
        for val in list_obj:
            skew += (val - mean_) ** 3
            skew = skew / n if not sample else n * skew / ((n - 1)*(n - 1) * SD_ ** 3)

        return skew
    
    def kurtosis(self, list_obj, sample = False):
        mean_ = self.mean(list_obj)
        kurt = 0
        SD_ = self.SD(list_obj, sample)
        n = len(list_obj)
        for x in list_obj:
            kurt += (x - mean_) ** 4
        kurt = kurt / (n * SD_ ** 4) if not sample else  n * (n + 1) * kurt / \
        ((n - 1) * (n - 2) * (SD_ ** 4)) - (3 *(n - 1) ** 2) / ((n - 2) * (n - 3))

        return kurt