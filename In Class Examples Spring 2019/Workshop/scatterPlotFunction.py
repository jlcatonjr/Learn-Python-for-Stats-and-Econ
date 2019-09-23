import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.backends.backend_pdf import PdfPages

def four_dim_scatter(data, year, x_name, y_name, c_name, s_name, smin=1, smax=10, figsize = (16, 10),
                 index_name = "Year", color_bar = "Dark2",discrete_color = False, pp = None):


    # select a subset of the data
    data_year = data[(data.index.get_level_values(index_name) == year)][plot_vars]
    # remove any row with nan value
    data_year = data_year.dropna( thresh =len(data_year.columns))

# size is not readily adjusted with df.plot.scatter()
#    data_year.plot.scatter(x="Rank",y="Government Consumption",
#                           c="Quartile", colormap = "viridis", 
#                           s = 0)
    # Create a figure and axis; choose size of the figure
    fig, ax = plt.subplots(figsize=figsize)
    
    # set plot values before hand, easier to interpret
    x = data_year[x_name]
    y = data_year[y_name]
    c = data_year[c_name]
    s = data_year[s_name]

    #chooses color schema, number of colors
    if discrete_color:
        color_divisions = len(set(data[c_name].dropna()))
        cmap = plt.cm.get_cmap(color_bar, color_divisions)
    else:
        cmap = plt.cm.get_cmap(color_bar)
    # use ax to plot scatter()
    scatter = ax.scatter(x=x,y=y,s=s,c=c,cmap=cmap)
    
    # create legend for scatter dot sizes
    # first build blank plots with desired sizes for legend
    smid = (smin + smax)  / 2
    gmin = plt.scatter([],[], s=10, marker='o', color='#555555')
    gmid = plt.scatter([],[], s=smid / 4, marker='o', color='#555555')                  
    gmax = plt.scatter([],[], s=smax / 4, marker='o', color='#555555')
    # create legend for plot size
    ax.legend((gmin,gmid,gmax),
       ("", s_name, ""),
       # bbox_to_anchor and loc set position of legend
       bbox_to_anchor=(0, -0.17),
       loc='lower left',
       fontsize=12)

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
    cbar.set_label(c_name, size=20)

    # set tick line length to 0
    ax.tick_params(axis=u'both', which=u'both',length=0)
    # set axis value labels fontsize
    plt.xticks(fontsize = 20)
    plt.yticks(fontsize = 20)
    # set axis range
    plt.xlabel(x_name,fontsize = 20)
    plt.ylabel(y_name, fontsize = 20)
    plt.xlim(3,10)
    plt.ylim(3,10)

    # Make title year for each scatter plot
    plt.title(str(year)[:4], fontsize = 30)    
    plt.show()
    if pp != None:
        pp.savefig(fig, bbox_inches = "tight")
    plt.close()

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

pp = PdfPages("Scatter Plots.pdf")
x = "Sound Money"
y ="Government Consumption"
c = "Quartile"
s = "RGDP Per Capita"

#for year in years:
#    four_dim_scatter(data, year, x, y, c, s,smin, smax, index_name = "Year", discrete_color=True, pp=pp)
pp.close()
    
data_year = data[(data.index.get_level_values("Year") == "2000")][plot_vars]
# remove any row with nan value
data_year = data_year.dropna( thresh =len(data_year.columns))

fig, ax = plt.subplots(figsize=(15,10))

plt.scatter(x = data_year[x], y = data_year[y], s = data_year[s])
plt.show()
