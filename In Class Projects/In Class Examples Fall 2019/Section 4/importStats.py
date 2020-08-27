import stats

stats_lib = stats.Stats()
list1 = [3, 6, 9, 12, 15]
list2 = [i ** 2 for i in range(3,8)]
print("sum list1 and list2", stats_lib.total(list1 + list2))
print("mean list1 and list2", stats_lib.mean(list1 + list2))
print("median list1 and list2", stats_lib.median(list1 + list2))
print("mode of list1 and list2", stats_lib.mode(list1 + list2))
print("variance of list1 and list2", stats_lib.variance(list1 + list2))
print("standard deviation of list1 and list2", 
      stats_lib.SD(list1 + list2))
print("covariance of list1 and list2 (separate)", 
      stats_lib.covariance(list1, list2))
print("correlation of list1 and list2 (separate)", 
      stats_lib.correlation(list1, list2))
print("skewness of list1 and list2", stats_lib.skewness(list1 + list2))
print("kurtosis of list1 and list2", stats_lib.kurtosis(list1 + list2))