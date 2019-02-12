#stats.py

class Stats():
    def __init__(self):
        self = self
            
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


list1 = [1,4,7,33,5,4,22,55,4,55,4,32]  
list2 = [4,8,22,1,9,43,3,2,1,99,3,10]            

stats = Stats()  
total1 = stats.total(list1)  
total2 = stats.total(list2)  
mean1 = stats.mean(list1)  
mean2 = stats.mean(list2)  
mode1 = stats.mode(list1)  
mode2 = stats.mode(list2)  
median1 = stats.median(list1)  
median2 = stats.median(list2)  
variance1 = stats.variance(list1)  
variance2 = stats.variance(list2)  
standard_deviation1 = stats.SD(list1)  
standard_deviation2 = stats.SD(list2)  
covariance_pop = stats.covariance(list1, list2)  
covariance_sample = stats.covariance(list1, list2, True)  
correlation = stats.correlation(list1, list2)  
skewness_pop1 = stats.skewness(list1)  
skewness_pop2 = stats.skewness(list2)  
skewness_sample1 = stats.skewness(list1, True)  
skewness_sample2 = stats.skewness(list2, True)  
kurtosis_pop1 = stats.kurtosis(list1)  
kurtosis_pop2 = stats.kurtosis(list2)  
kurtosis_sample1 = stats.kurtosis(list1, True)  
kurtosis_sample2 = stats.kurtosis(list2, True)  

print("Total1:", total1)
print("Total2:", total2)
print("Mean1:", mean1)
print("Mean2", mean2)
print("Mode1:", mode1)
print("Mode2:", mode2)
print("Median1:", median1)
print("Median2:", median2)
print("Variance1:", variance1)
print("Variance2:", variance2)
print("Standard Deviation1:", standard_deviation1)
print("Standard Deviation2:", standard_deviation2)
print("Covariance (Population):", covariance_pop)
print("Covariance (Sample):", covariance_sample)
print("Correlation (Population):", correlation)
print("SkewnessPop1 (Population):", skewness_pop1)
print("SkewnessPop2 (Population):", skewness_pop2)
print("SkewnessSample1 (Sample):", skewness_sample1)
print("SkewnessSample2 (Sample):", skewness_sample2)
print("Kurtosis1 (Population):", kurtosis_pop1)
print("Kurtosis2 (Population):", kurtosis_pop2)
print("Kurtosis1 (Sample):", kurtosis_sample1)
print("Kurtosis2 (Sample):", kurtosis_sample2)
