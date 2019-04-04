#stats.py

class Stats():
    def __init__(self):
        pass
            
    def total(self, list_obj):
        total = 0 
        n = len(list_obj)
        for i in range(n):
            total += list_obj[i]
        return total
    
    def mean(self, list_obj):
        n = len(list_obj)
        mean = self.total(list_obj) / n
        return mean
    
    def median(self, list_obj):
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
            median = self.mean(list_obj[middle_num1:middle_num2 + 1])
        
        return median
    
    def mode(self, list_obj):
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
    
    def variance(self, list_obj, sample = False):
        """ Step 1 """
        list_mean = self.mean(list_obj)
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
    
    def SD(self, list_obj, sample = False):
        list_variance = self.variance(list_obj, sample)
        list_SD = list_variance ** (1/2)
        
        return list_SD
    
    def covariance(self, list1, list2, sample = False):

        len_list1 = len(list1)
        len_list2 = len(list2)
        if len_list1 == len_list2:
            mean_list1 = self.mean(list1)
            mean_list2 = self.mean(list2)
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
        
    def correlation(self, list1, list2):
        cov = self.covariance(list1, list2)
        SD1 = self.SD(list1)
        SD2 = self.SD(list2)
        corr = cov / (SD1 * SD2)
        return corr

    def skewness(self, list_obj, sample = False):
        mean_ = self.mean(list_obj)
        skew = 0
        n = len(list_obj)
        for x in list_obj:
            skew += (x - mean_) ** 3
        skew = skew / n if not sample else n * skew / ((n - 1) * (n - 2))
        SD_ = self.SD(list_obj, sample)
        skew = skew / (SD_ ** 3)           
        return skew
    
    def kurtosis(self, list_obj, sample = False):
        mean_ = self.mean(list_obj)
        kurt = 0
        n = len(list_obj)
        for x in list_obj:
            kurt += (x - mean_) ** 4
        SD_ = self.SD(list_obj, sample)
        kurt = kurt / n if not sample else n * (n + 1) * kurt / ((n - 1) * \
            (n - 2)) - (3 * (n - 1) ** 2) / ((n - 2) * (n - 3))
        kurt = kurt / SD_ ** 4
        return kurt


