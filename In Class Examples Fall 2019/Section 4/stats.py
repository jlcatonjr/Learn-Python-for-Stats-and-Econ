#stats.py
class Stats():
    def __init__(self):
        print("You created an instance of Stats")
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
        list_obj = sorted(list_obj)
        if n % 2 != 0:
            middle_index = int((n - 2) / 2)
            median = list_obj[middle_index]
        else:
            upper_middle_index = int(n / 2)
            lower_middle_index = upper_middle_index - 1
            median = self.mean(\
                list_obj[lower_middle_index:upper_middle_index + 1])
        
        return median
    
    def mode(self, list_obj):
        max_count = 0
        counter_dict={}
        for value in list_obj:
            counter_dict[value] = 0
        for value in list_obj:
            counter_dict[value] += 1
        count_list = list(counter_dict.values())
        max_count = max(count_list)
        mode = [key for key in counter_dict if counter_dict[key] == max_count]
        
        return mode
    
    def variance(self, list_obj, sample = False):
        list_mean = self.mean(list_obj)
        n = len(list_obj)
        sum_sq_diff = 0
        for val in list_obj:
            sum_sq_diff += (val - list_mean) ** 2
        if sample == False:
            variance = sum_sq_diff / n
        else:
            variance = sum_sq_diff / (n - 1)
        
        return variance
    
    def SD(self, list_obj, sample = False):
        SD = self.variance(list_obj, sample) ** (1/2)
        return SD
    
    def covariance(self, list_obj1, list_obj2, sample = False):
        mean1 = self.mean(list_obj1)
        mean2 = self.mean(list_obj2)
        cov = 0
        n1 = len(list_obj1)
        n2 = len(list_obj2)
        
        if n1 == n2:
            for i in range(n1):
                cov += (list_obj1[i] - mean1) * \
                    (list_obj2[i] - mean2)
            if sample == False:
                cov = cov / n1
            else:
                cov = cov / (n1 - 1)
            return cov
        else:
            print("List lengths are not equal")
            print("List1 observations:", n1)
            print("List2 observations:", n2)
    
    def correlation(self, list_obj1, list_obj2):
        cov = self.covariance(list_obj1, list_obj2)
        SD1 = self.SD(list_obj1)
        SD2 = self.SD(list_obj2)
        corr = cov / (SD1 * SD2)        
        
        return corr
    
    def skewness(self, list_obj, sample = False):
        mean_ = self.mean(list_obj)
        skew = 0
        n = len(list_obj)
        for val in list_obj:
            skew += (val - mean_) ** 3
        skew = skew / n if not sample else n * skew / ((n-1) * (n - 2))
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
        kurt = kurt / (n * SD_ ** 4) if not sample else \
            n * (n + 1) * kurt / ((n - 1) * (n - 2) * (SD_ ** 4)) -\
            (3 *(n - 1) ** 2) / ((n - 2) * (n - 3))
            
        return kurt