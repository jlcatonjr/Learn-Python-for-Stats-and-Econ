#%matplotlib notebook
import ipywidgets as ipw 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib.ticker as mtick
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import geopandas as gpd

class livePlot(): 
    def __init__(self, geo_data, dates):
        def format_map():
            size = "5%" 
            sm = cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
            # empty array for the data range
            sm._A = []
            # make space for colorbar
            divider = make_axes_locatable(self.ax)
            cax = divider.append_axes("right", size = size, pad = 0.1)
            # add colorbar to figure
            cbar = self.fig.colorbar(sm, cax=cax, cmap = self.cmap)
            cbar.ax.tick_params(labelsize=18)
            vals = list(cbar.ax.get_yticks())
            vals.append(self.vmax)
            #if "Daily" not in key: 
            vals[0] = 0
            # format display of values on colorbar
            # if log:
            #     cbar.ax.yaxis.set_major_formatter(mtick.LogFormatter())
            # else:
            cbar.ax.yaxis.set_major_formatter(mtick.Formatter())
            # format colorbar values as int
            cbar.ax.set_yticklabels([int(x) for x in vals])
            cbar.ax.set_ylabel(self.key, fontsize = 20)


        def interact():
            def update(date_index = 0):
                date = self.dates[date_index]
                # self.ax.clear()
                plt.cm.ScalarMappable(cmap=self.cmap, norm=self.norm)
                plot_df = self.geo_data[self.geo_data.index.get_level_values("date")==date]
                plot_df.plot(ax=self.ax, cax = self.ax, column=self.key, vmin=self.vmin ,vmax = self.vmax, 
                             cmap = self.cmap, legend=False, linewidth=.5, edgecolor='lightgrey', 
                             norm = self.norm)
                self.ax.set_title(str(date)[:10] + "\n" + "COVID-19 in the U.S.", fontsize = 30)
        
            self.widget = ipw.interact(update, 
                          date_index = ipw.IntSlider(
                            value=len(self.dates) - 1,
                            min=0,
                            max=len(self.dates) - 1,
                            step=1,
                            description='Date Index:',
                            disabled=False,
                            continuous_update=True,
                            orientation='horizontal',
                            readout=True,
                            readout_format="d"))

        plt.rcParams["font.size"] = 20
        self.fig, self.ax = plt.subplots(figsize = (8, 6))
        self.geo_data = geo_data
        self.dates = dates  
        self.date = self.dates[-1]
        self.key="Cases per Million"
        self.vmin, self.vmax = 0, geo_data[self.key].max()
        self.cmap = cm.get_cmap('Reds', 10)
        self.norm = cm.colors.Normalize(vmin = self.vmin, vmax = self.vmax)
        # format_map()
        interact()

    


        # self.maxx = 1000
        # self.maxy = 130
        # self.ax.set_xlim(0, self.maxx)
        # self.ax.set_ylim(0, self.maxy)
        # plt.xticks([])
        # plt.yticks([])

        # self.M = 10 ** 3
        # self.V = 8

        # self.y = np.linspace(1, self.M, self.M)
        # self.y0 = 10 ** 2 * 5

        # self.AD, = self.ax.plot(self.y, self.M * self.V / self.y)
        # self.LRAS = self.ax.axvline(self.y0)

        # x_int, y_int = self.get_intersect(self.AD, self.LRAS, line2_vert = True)
        # self.h_line_intersect = self.ax.axhline(y_int, xmin = 0, xmax = x_int, 
        #                               ls = "--", color = "k")

        # self.text_vert_shift = 1
        # self.text_horiz_shift = 20
        # self.P_text = self.ax.text(-50, y_int, "$P$")
        # self.AD_text = self.ax.text(900, self.AD.get_ydata()[900] + self.text_vert_shift * -2, "$AD$")
        # self.LRAS_text = self.ax.text(self.LRAS.get_xdata(orig=False)[0] + self.text_horiz_shift ,
        #                               110, "$LRAS$")
        # self.y0_text = self.ax.text(self.LRAS.get_xdata(orig=False)[0] - self.text_horiz_shift * .75, -10, "$y$")
        # # self.MV_val_text = self.ax.text(1001, 100, "MV =" +str(self.M * self.V))
        # # self.str_vals = "MV =" +str(int(self.M * self.V)) + "   P =" + str(int(self.M * self.V / self.y0)) + "   y ="+ str(int(self.y0))
        # self.show_vals = self.ax.text(1, self.maxy * 1.03, 
        #                               "MV =" +str(int(self.M * self.V)) + "    P =" + str(int(self.M * self.V / self.y0)) + "    y ="+ str(int(self.y0)),
        #                               fontsize = 14) 

        
  

    # def get_intersect(self, line1, line2, line2_vert = False):
    #     if line2_vert == False:
    #         x = np.argwhere(np.diff(np.sign(line1 - line2))).flatten()
    #     else:
    #         line1_data = line1.get_data()
    #         # set orig = False or else list reads as float
    #         line2_xdata = line2.get_xdata(orig=False)[0]
    #         dist = [np.abs(i - line2_xdata) for i in line1_data[0]]
    #         min_dist = min(dist)
    #         x = dist.index(min_dist)
    #         y = line1_data[1][x]

    #     return x, y
