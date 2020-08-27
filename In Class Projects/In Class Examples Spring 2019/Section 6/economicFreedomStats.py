#economicFreedomStats.py
import pandas as pd
import stats
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages

data = pd.read_csv("index2017_data.csv", index_col = ["Country Name"], 
                   encoding="ISO-8859-1")
# Drop columns that have only NA values
data = data.dropna(axis = 1, thresh = 1)
# Drop rows that have only NA values
data = data.dropna(axis = 0, thresh = 1)

# some columns are not needed for the purposes of this exercise, so we 
# will drop them
skip_keys = ["CountryID", "Region", "WEBNAME", "Country"]
data_for_stats = data.drop(skip_keys, axis=1)
#Drop data that does not include observations for every category
data_for_stats = data_for_stats.dropna(thresh = len(data_for_stats.columns))

# Data is imported as string, so we need to transform the data
# Some rows have dollar signs and commas. These should be removed
# we use str.replaced() to replace these characters with an empty string
for key in data_for_stats:
    try:
        data_for_stats[key] = data_for_stats[key].str.replace(r'[$,]', '')
        print("$ or , removed from:", key )
    except:
        print(key, "not transformed:", data[key].dtype)


#Drop keys with non_numeric data
# transform strings to values using pd.to_numeric(df, errors="force")
for key in data_for_stats:
    data_for_stats[key] = pd.to_numeric(data_for_stats[key], errors="force")

## Next, we create dictionaries that will hold statistics for each variable
#    # or pair of variables in the case of cov and corr statistics
stats_ = stats.Stats()
stats_dict = {}
cov_dict = {}
corr_dict = {}

# for each key, we create statistics for mean, median, variance, SD, skewness,
# and kurtosis. Then, we create an additional matrix of values for that shows
# the cov and corr between key1 and all other keys.

for key1 in data_for_stats:
    # to use the functions from stats requres that we call lists, not Series
    # so a list of values is create for each variable (key1) in the dataframe
    vec = data_for_stats[key1].values.tolist()
    stats_dict[key1] = {}
    stats_dict[key1]["mean"] = stats_.mean(vec)
    stats_dict[key1]["median"] = stats_.median(vec)
    stats_dict[key1]["variance"] = stats_.variance(vec)
    stats_dict[key1]["standard deviation"] = stats_.SD(vec, True)
    stats_dict[key1]["skewness"] = stats_.skewness(vec, True)
    stats_dict[key1]["kurtosis"] = stats_.kurtosis(vec,True)
    cov_dict[key1] = {}
    corr_dict[key1] = {}
    for key2 in data_for_stats:
        vec2 = data_for_stats[key2].values.tolist()
        print(key1, key2)
        cov_dict[key1][key2] = stats_.covariance(vec, vec2, True)
        corr_dict[key1][key2] = stats_.correlation(vec, vec2)

# convert stats, cov, and corr dictionaries to pandas DataFrames
stats_DF = pd.DataFrame(stats_dict)
cov_DF = pd.DataFrame(cov_dict).sort_index(axis=1)
corr_DF = pd.DataFrame(corr_dict).sort_index(axis=1)

# output DataFrames to CSV
stats_DF.to_csv("econFreedomStatsByCategory.csv")
cov_DF.to_csv("econFreedomCovMatrix.csv")
corr_DF.to_csv("econFreedomCorrMatrix.csv")
data_for_stats.to_csv("cleanedEconFreedomData.csv")

# Save plots in a pdf using PdfPages
pp = PdfPages("Economic Freedom Plots.pdf")
# Set size of font used unless otherwise specified
plt.rcParams.update({'font.size': 26})
# select subset of variables to visualize
scatter_cats = ["World Rank", "2017 Score", "Property Rights", "Judical Effectiveness", 
                "5 Year GDP Growth Rate (%)", "GDP per Capita (PPP)"]
scatter_data = data_for_stats[scatter_cats]

# create scatterplots that use color to vizualize a third dimension
#for key1 in scatter_data:
#    for key2 in scatter_data:
#        # do not create visualization if key1 == key2
#        if key1 != key2:
#            for key3 in scatter_data:
#                # do not create visualization if key1 == key3,
#                # or if key2 == key3
#                if key1 != key3 and key2 != key3:
#                    # Choose figure size and save ax as object
#                    fig, ax = plt.subplots(figsize = (20,20))
#                    # each point represents a an observation with 
#                    # 3 different values: key1 on the horiz ax, 
#                    # key2 on the vert ax, and key3 as color
#                    scatter_data.plot.scatter(x = key1, y = key2, c = key3,
#                                  s = 50, alpha = .7, colormap = "viridis",
#                                  ax=ax).get_figure()
#                    # Make values on x-axis vertical
#                    plt.xticks(rotation = 90)
#                    # Remove tick lines
#                    plt.setp(ax.get_xticklines(), visible=False)
#                    plt.setp(ax.get_yticklines(), visible=False) 
##                    plt.show()
#                    pp.savefig(fig, bbox_inches = "tight")
#                    plt.close()
            
# Create a figure to visualize a corr table
fig, ax = plt.subplots(figsize=(20,20))
# Use the same subset of variable from the above scatter plots
select_corr_DF = corr_DF.ix[scatter_cats][scatter_cats]
# use ax.imshow() to create a heatmap of correlation values
# seismic mapping shows negative values as blue and positive values as red
im = ax.imshow(select_corr_DF, cmap = "seismic")

# create a list of lables, stacking each word in a lable by replacing " " with 
# "\n"
labels = select_corr_DF.keys()
tick_labels = [lab.replace(" ", "\n") for lab in labels]
# prepare space for label of each column
x_ticks = np.arange(len(labels))
# select labels and rotate them 90 degreees so that they are vertical
plt.xticks(x_ticks, tick_labels , fontsize = 20, rotation=90) 
# prepare space for label of each row
y_ticks = np.arange(len(labels))
# select labels
plt.yticks(y_ticks, tick_labels, fontsize = 20)

# show values in each tile of the heatmap
for i in range(len(labels)):
    for j in range(len(labels)):
        text = ax.text(i, j, str(round(select_corr_DF.values[i][j],2)),
                       ha="center", va="center", color="w")
# Create title with Times New Roman Font
title_font = {'fontname':'Times New Roman'}
plt.title("Correlation", fontsize = 50, **title_font)
# Call scale to show values of colors
fig.colorbar(im)
plt.show()
pp.savefig(fig, bbox_inches="tight")
plt.close()

# Create a figure showing scatterplots given in scatter_cats
fig_len = 50
fig, ax = plt.subplots(figsize=(fig_len,fig_len))
# Use fig_len to dictate fig_size, adjust size of font, size of dots, etc...
plt.rcParams.update({'font.size': int(.7 * fig_len)})
axes = pd.plotting.scatter_matrix(scatter_data,alpha = .5, 
                                  ax = ax,
                                  s = fig_len ** 1.5)

# tight layout improves layout of text and plots in the figure
plt.tight_layout()
plt.show()
pp.savefig(fig, bbox_inches = "tight")
pp.close()
plt.savefig(r"scatterPlots.png")
plt.close()