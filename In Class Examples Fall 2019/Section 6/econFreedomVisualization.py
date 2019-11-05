#econFreedomVisualization.py
import pandas as pd
import numpy as np
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
#                        plt.show()
                        pp.savefig(fig, bbox_inches = "tight")
                        plt.close()
                        
def corr_matrix_heatmap(data, pp):
    #Create a figure to visualize a corr matrix
    fig, ax = plt.subplots(figsize = (20,20))
    # use ax.imshow() to create a heatmap of correlation values
    # seismic mapping shows negative values as blue and positive values as red
    extent = (-0.5,len(data.keys()) - .5, -0.5, len(data.keys()) - .5)
    im = ax.imshow(data.values, cmap = "seismic", extent = extent)
    # create a list of labels, stacks each word in a label by replacing " " 
    # with "\n"
    labels = data.keys()
    num_vars = len(labels)
    tick_labels = [lab.replace(" ", "\n") for lab in labels]
    # adjust font size according to the number of variables visualized
    tick_font_size = 120 / num_vars
    val_font_size = 200 / num_vars
    # prepare_ space for label of each column
    x_ticks = np.arange(len(labels))
    # select labels and rotate them 90 degrees so that they are vertical
    plt.xticks(x_ticks, tick_labels, fontsize = tick_font_size, rotation = 90)
    # prepare space for label of each row
    y_ticks = np.arange(len(labels))
    # select labels
    plt.yticks(y_ticks, tick_labels, fontsize = tick_font_size)
    # show values in each tile of the heatmap
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(i, j, str(round(data.values[i][j], 2)),
                           fontsize = val_font_size, ha = "center",
                           va = "center", color = "w")
    #Create title with Times New Roman Font
    title_font = {"fontname":"Times New Roman"}
    plt.title("Correlation", fontsize = 50, **title_font)
    # Call scale to show value of colors
    cbar = fig.colorbar(im)
    cbar.set_clim(-1, 1)
    plt.show()
    pp.savefig(fig, bbox_inches="tight")
    plt.close()
    
def formatted_scatter_matrix(data, pp):
    # Create a figure showing scatterplots given in scatter_cats
    fig_len = 15
    fig, ax = plt.subplots(figsize = (fig_len, fig_len))
    # Use fig_len to dictate fig_size, adjust size of font, size of dots, etc...
    num_vars = len(data.keys())
    fontsize = 65 / num_vars
    plt.rcParams.update({"font.size":fontsize})
    pd.plotting.scatter_matrix(data, alpha = .5, s=108 / num_vars,
                               ax = ax)
    plt.tight_layout()
    plt.show()
    pp.savefig(fig, bbox_inches = "tight")
    
data = pd.read_csv("cleanedEconFreedomData.csv", index_col = ["Country Name"])
corr_data = pd.read_csv("econFreedomCorrMatrix.csv", index_col = [0])
# Save plots in a pdf using PdfPages
pp = PdfPages("Economic Freedom Plots.pdf")
# Set size of font used unless otherwise specified
plt.rcParams.update({"font.size": 26})
# select subset of variables to visualize in scatter plot
scatter_cats = ["World Rank", "2017 Score", "Property Rights",
                "Judical Effectiveness"]#, "5 Year GDP Growth Rate (%)"]
#                "GDP per Capita (PPP)", "Unemployment (%)", "Inflation (%)"]
select_data = data[scatter_cats]
# .loc calls index instead of column
select_corr_data = corr_data.loc[scatter_cats][scatter_cats]
print(select_corr_data)
color_dim_scatter(select_data, pp)
corr_matrix_heatmap(select_corr_data, pp)
formatted_scatter_matrix(select_data, pp)

pp.close()