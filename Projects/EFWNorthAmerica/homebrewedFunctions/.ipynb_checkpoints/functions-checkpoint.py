import time
import numpy as np
import pandas as pd
import pandas_datareader.data as web
import pingouin
import matplotlib.pyplot as plt
import datetime
from linearmodels import PanelOLS
from linearmodels.panel import compare

class info_criterion():
    ## Thank you Abi Idowu
    # Function to calculate AIC
    def calculate_aic(self, n, rss, k):
        return n * np.log(rss / n) + 2 * k
    
    # Function to calculate BIC
    def calculate_bic(self, n, rss, k):
        return n * np.log(rss / n) + k * np.log(n)
    
    # Function to calculate HQIC
    def calculate_hqic(self, n, rss, k):
        return n * np.log(rss / n) + 2 * k * np.log(np.log(n))

def gather_data(data_codes, 
                start, 
                end = datetime.datetime.today(), 
                freq = "M"):
    i = 0
    # dct.items() calls key and value that key points to
    for key, val in data_codes.items():
        time.sleep(.51)
        if i == 0:
            # Create dataframe for first variable, then rename column
            df = web.DataReader(
                val, "fred", start, end).resample(freq).mean()
            df.rename(columns = {val:key}, inplace = True) 
            # setting i to None will cause the next block of code to execute,
            # placing data within df instead of creating a new dataframe for
            # each variable
            i = None
        else:
            # If dataframe already exists, add new column
            df[key] = web.DataReader(val, "fred", start, end).resample(freq).mean()

    return df

def save_dict_of_dfs_to_excel(dict_of_dfs, filename):
    """
    Save a dictionary of DataFrames to an Excel file, with each DataFrame in a separate sheet.

    Parameters:
    dict_of_dfs (dict): A dictionary where keys are sheet names and values are DataFrames.
    filename (str): The path to the output Excel file.
    """
    with pd.ExcelWriter(filename) as writer:
        for sheet_name, df in dict_of_dfs.items():
            df.reset_index().to_excel(writer, sheet_name=sheet_name)
    print(f"File saved as {filename}")

def plot_scatter_corr(plot_df, title, corr="corr", **kwargs):
    corr_df = getattr(plot_df, corr)().round(2)
    num_keys = len(plot_df.keys())
    fig, axs = plt.subplots(num_keys, num_keys, figsize=(20,20))
    
    for i, key1 in enumerate(plot_df.keys()):
        for j, key2 in enumerate(plot_df.keys()):
            
            if i < j:
                ax = axs[j][i]
                plot_df.plot.scatter(x=key1, y=key2, ax=ax, **kwargs)
                # Remove color bar label if 'c' is in kwargs
                if 'c' in kwargs:
                    cbar = ax.collections[0].colorbar
                    if cbar is not None:
                        cbar.set_label('')
                        cbar.set_ticklabels([])
            elif i > j:
                ax = axs[j][i]
                ax.text(.5, .5, corr_df.astype(str).loc[key2, key1],
                        ha="center", va="center", fontsize=28)
                ax.set_xticklabels([])
            else:
                ax = axs[i][j]
                plot_df[[key1]].hist(density=True, ax=ax)
                if i == 0: ax.set_ylabel(key1)
            
            if i > 0:
                ax.set_ylabel("")
                ax.set_yticklabels([])
            else:
                ax.set_ylabel(key2.replace(" ", "\n"), fontsize=24)
            if j < num_keys - 1: 
                ax.set_xticklabels([])
            if j > 0:
                ax.set_title("")
            else:
                ax.set_title(key1.replace(" ", "\n"), fontsize=24)
            ax.set_xlabel("")
    
    plt.suptitle(title, fontsize=40, y=1.025)
    return fig, ax



def compare_regs_plot(compare_regs,y, variant="", title =""):
    title = f"y = {y}" if title == "" else title
    hlines = {"params":[0],
              "tstats":[0],
              "pvalues":[0.05, 0.1]}
    fig, axs = plt.subplots(2, 1, figsize = (20,6))
    stat_names = ("params", "pvalues")
    for i, stat in enumerate(stat_names):
        ax = axs[i]
        getattr(compare_regs, stat).plot.bar(ax = axs[i], legend = False)
        ax.set_ylabel(stat.title())
        
        if i == 0:
            ax.legend(loc = 1, ncols = 4, bbox_to_anchor = (.85,1.43), fontsize = 18)
        if i < len(stat_names) - 1:
            ax.set_xticklabels([])
            ax.set_xlabel("")
        else:
            ax.set_xticklabels([x.replace(" ", "\n") for x in compare_regs.params.index], rotation = "horizontal", fontsize = 20)

        for yval in hlines[stat]:
            ax.axhline(y = yval, ls = "--", 
                       linewidth = 2, color = "k")

        plt.suptitle(f"{variant}: {title}", y = 1.2)
        
def plot_r2(r2_df, r2s, key, variant):
    num_plots = 3
    fig, axs = plt.subplots(num_plots, 1, figsize = (20,10))
    for n, r2 in enumerate(r2s):
        ax = axs[n]
        plot_df = r2_df[r2_df["r2"] == r2]
        plot_df.plot(x = "y", y = list(r2_df.keys())[2:], kind = "bar", legend = False, ax = ax)
        if n == 0: 
            ax.legend(loc = 1, ncols = 4, bbox_to_anchor = (.85,1.4), fontsize = 18)        
        if n + 1 == num_plots: 
            ax.set_xticklabels([x for x in ax.get_xticklabels()], rotation = "horizontal", fontsize = 20)
        else:
            ax.set_xticklabels([])
            ax.set_xlabel("")

        ax.set_ylabel(r2.replace("_", "\n").title(), fontsize = 20)
        ax.set_yticklabels(ax.get_yticklabels(), fontsize = 14)
        plt.suptitle(f"{variant}: {key}\n$r^2$ Measures", y = 1.09)
        ax.axhline(0, color = "k", ls = "-", linewidth = 2)
        # ax.set_xticklabels(ax.get_xticklabels(), rotation = 90)