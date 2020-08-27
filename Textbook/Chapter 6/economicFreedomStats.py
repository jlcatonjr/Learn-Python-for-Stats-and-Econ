#economicFreedomStats.py
import pandas as pd
import stats

data = pd.read_excel("index2017_data.xls", index_col = [1])

# some columns are not needed for the purposes of this exercise, so
# we drop them
skip_keys = ["CountryID", "Region", "WEBNAME", "Country"]
data_for_stats = data.drop(skip_keys, axis = 1)
#Drop rows that do not include observations for every category
data_for_stats = data_for_stats.dropna(thresh = len(data_for_stats.columns))

# Next, we create dictionaries that will hold statistics for each variable
# or pair of variables in the case of cov and corr
stat = stats.Stats()
stats_dict = {}
cov_dict = {}
corr_dict = {}

for key1 in data_for_stats:
    # to use the functions from stats requires that we call lists, not Series
    # so a list of values is create for each variable (key1) in the dataframe
    vec1 = data_for_stats[key1]
    stats_dict[key1] = {}
    stats_dict[key1]["mean"] = stat.mean(vec1)
    stats_dict[key1]["median"] = stat.median(vec1)
    stats_dict[key1]["variance"] = stat.variance(vec1)
    stats_dict[key1]["standard deviation"] = stat.SD(vec1, sample = True)
    stats_dict[key1]["skewness"] = stat.skewness(vec1, sample = True)
    stats_dict[key1]["kurtosis"] = stat.kurtosis(vec1, sample = True)
    cov_dict[key1] = {}
    corr_dict[key1] = {}
    for key2 in data_for_stats:
        vec2 = data_for_stats[key2]
        cov_dict[key1][key2] = stat.covariance(vec1, vec2, sample = True)
        corr_dict[key1][key2] = stat.correlation(vec1, vec2)   

#convert stats, cov, and corr dictionaries to pandas DataFrames
stats_DF = pd.DataFrame(stats_dict)
cov_DF = pd.DataFrame(cov_dict).sort_index(axis=1)
corr_DF = pd.DataFrame(corr_dict).sort_index(axis=1)

# output DataFrames to CSV
stats_DF.to_csv("econFreedomStatsByCategory.csv")
cov_DF.to_csv("econFreedomCovMatrix.csv")
corr_DF.to_csv("econFreedomCorrMatrix.csv")
data_for_stats.to_csv("cleanedEconFreedomData.csv")
        
print(stats_dict)
print(cov_dict)
print(corr_dict)
#print(data_for_stats)