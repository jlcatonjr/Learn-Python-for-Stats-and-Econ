#econFreedomVisualization.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def color_dim_scatter(data, pp):
    for key1 in data:
        for key2 in data:
            # do not use same variable for x and y dimension
            if key1 != key2:
                for key3 in data:
                    # do not create vizualization if key1 or key2
                    # equals key3
                    if key1 != key3 and key2 != key3:
                        # choose figure size and save ax as object
                        fig, ax = plt.subplots(figsize = (20,20))
                        # each point represents an observation with 3 different
                        # values: key1 on the horiz ax, key2 is on the vert ax,
                        # and key 3 as color
                        data.plot.scatter(x = key1, y = key2, c = key3, s = 50,
                                          alpha = .7, colormap = "viridis",
                                          ax = ax)
                        # Make values on x-axis vertical
                        plt.xticks(rotation = 90)
                        # Remove tick lines
                        plt.setp(ax.get_xticklines(), visible = False)
                        plt.setp(ax.get_yticklines(), visible = False)
                        plt.show()
                        pp.savefig(fig, bbox_inches = "tight")
                        plt.close()
                        
            # do not use

data = pd.read_csv("cleanedEconFreedomData.csv", index_col = ["Country Name"])
# Save plots in a pdf using PdfPages
pp = PdfPages("Economic Freedom Plots.pdf")
# Set size of font used unless otherwise specified
plt.rcParams.update({"font.size": 26})
# select subset of variables to visualize in scatter plot
scatter_cats = ["World Rank", "2017 Score", "Property Rights",
                "Judical Effectiveness", "5 Year GDP Growth Rate (%)",
                "GDP per Capita (PPP)"]
select_data = data[scatter_cats]
print(select_data.keys())
color_dim_scatter(select_data, pp)
pp.close()