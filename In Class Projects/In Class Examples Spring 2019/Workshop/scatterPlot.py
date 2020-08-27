import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

#changes background of plot
#plt.style.use('ggplot')


#import data
data = pd.DataFrame.from_csv("fraserDataWithRGDPPC.csv", index_col=[0,1])

# create list of each index set from multi index
years = list(sorted(set(data.index.get_level_values('Year'))))
country = list(sorted(set(data.index.get_level_values('ISO_Code'))))
#choose variables that will be plotted for each year in scatter
plot_vars = ["Sound Money", "Government Consumption", 
             "RGDP Per Capita","Quartile"]

# Normalize income so that 1 represents the maximum value of RGDP Per Capita
# This will allow dot to be easily adjusted
data["RGDP Per Capita"] = data["RGDP Per Capita"] / max(data["RGDP Per Capita"]) * 1000
smin = min(data["RGDP Per Capita"])
smax = max(data["RGDP Per Capita"])
smid = (smin + smax)  / 2

pp = PdfPages("Scatter Plots.pdf")

for year in years:    
    # select a subset of the data
    data_year = data[(data.index.get_level_values('Year') == year)][plot_vars]
    # remove any row with nan value
    data_year = data_year.dropna( thresh =len(data_year.columns))

# size is not readily adjusted with df.plot.scatter()
#    data_year.plot.scatter(x="Rank",y="Government Consumption",
#                           c="Quartile", colormap = "viridis", 
#                           s = 0)
    # Create a figure and axis; choose size of the figure
    fig, ax = plt.subplots(figsize = (16, 10))
    
    # set plot values before hand, easier to interpret
    x = data_year["Sound Money"]
    y = data_year["Government Consumption"]
    c = data_year["Quartile"]
    color_divisions = 4
    s = data_year["RGDP Per Capita"]
    #chooses color schema, number of colors
    cmap = plt.cm.get_cmap('Dark2', color_divisions)
    # use ax to plot scatter()
    scatter = ax.scatter(x=x,y=y,s=s,c=c,cmap=cmap)
    
    # create blank plots with desired sizes for legend
    gmin = plt.scatter([],[], s=10, marker='o', color='#555555')
    gmid = plt.scatter([],[], s=smid / 4, marker='o', color='#555555')                  
    gmax = plt.scatter([],[], s=smax / 4, marker='o', color='#555555')
    # create legend for plot size
    ax.legend((gmin,gmid,gmax),
       ("", "Real GDP Per Capita", ""),
       bbox_to_anchor=(0, -0.17),
       scatterpoints=1,
       loc='lower left',
       ncol=1,
       fontsize=12)
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    plt.xlim(3,10)
    plt.ylim(3,10)
    # include colorbar
    cbar = plt.colorbar(scatter)
    # this centers the number bar value labels
    # change some of the values passed to see what happens....
    tick_locs = (np.arange(1, color_divisions+1) + .82)*(color_divisions-1)/color_divisions
    cbar.set_ticks(tick_locs)
    # choose numbers 1 through 4 as colorbar labels
    cbar.set_ticklabels(np.arange(1,color_divisions+1))
    cbar.ax.tick_params(labelsize=20)
    # add general label to colorbar
    cbar.set_label("Economic Freedom Quartile", size=20)
    plt.xlabel("Sound Money",fontsize = 20)
    plt.ylabel("Goverment Corruption", fontsize = 20)
    # Make title year for each scatter plot
    plt.title(str(year)[:4], fontsize = 30)    
    plt.show()
    pp.savefig(fig, bbox_inches = "tight")
    plt.close()
pp.close()