#macroOLS.py
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.backends.backend_pdf import PdfPages
import statsmodels.api as sm

def OLSRegression(df,endogVar, exogVars):
    #Select endogenous data for Y
    Y = dataFrame[endogVar]
    #Select exogenous data for X
    X = dataFrame[exogVars]
    #Add column of ones for constant
    X = sm.add_constant(X)
    print(X)
    #Run regression
    model = sm.OLS(Y,X)
    #Save results of regression
    results = model.fit()
    return results

def plotValues(df,keys):
    df[keys].plot.line(figsize=(24,12), legend=False, secondary_y=keys[0])
    plt.title(str(keys) + "\n", fontsize=40)
#    plt.axhline(0)
#    plt.ylim([-10,10])
    plt.show()
    plt.close()

def scatterPlot(df, key1,key2,pp,start,end, title=""):
    fig,ax = plt.subplots(figsize=(24,12))
    plt.scatter(x=df[key1], y=df[key2], s = 5**2, c=range( int(matplotlib.dates.date2num(end))))
    plt.axhline(0, ls = "--", color="k", linewidth = 1)
    plt.axvline(0, ls="--", color="k", linewidth = 1)
    ax.set_xlabel(key1)
    ax.set_ylabel(key2)
#    ax.set_xlim(min(df[key1]) * .98, max(df[key1]) * 1.02)
#    ax.set_ylim(min(df[key2]) * .98, max(df[key2]) * 1.02)
    plt.colorbar()
    plt.set_cmap("plasma")
    # get the old tick labels (index numbers of the dataframes)
#    clb_ticks = [int(t.get_text()) for t in clb.ColorbarBase(]
    # convert the old, index, ticks into year-month-day format
#    new_ticks = df.index[clb_ticks].strftime("%Y-%m-%d")
#    clb.ax.yaxis.set_ticklabels(new_ticks)
    plt.savefig(str(start).replace(":","") + "-" + str(end).replace(":","")\
                + " " +\
                key1 + " " + key2 +' scatter '+'.png', bbox_inches="tight")

    plt.show()
    pp.savefig(fig, bbox_inches="tight")
    plt.close()



def buildSummaryCSV(csvSummary, csvName):    
    #Create a new csv file
    file = open(csvName + ".csv", "w")
    #write results in csv file
    file.write(csvSummary)
    #close CSV
    file.close()
    
pp = PdfPages("Gold Elasticities.pdf")  
start = datetime.datetime(1972, 1, 1)
end = datetime.datetime(2018, 8, 1)
dfDict = {}

dfDict["Data"] = web.DataReader("IPG21222N", "fred", start, end).resample("Q", how="mean")
dfDict["Data"] = dfDict["Data"].rename(columns = {"IPG21222N":"Gold Production"}) 
dfDict["Data"]["Price of Gold"] = web.DataReader("GOLDPMGBD228NLBM", "fred", start, end).resample("Q", how="mean")
dfDict["Data"]["% Change in Gold Production"] = (dfDict["Data"]["Gold Production"].diff() / dfDict["Data"]["Gold Production"])
dfDict["Data"]["% Change in Gold Price"] = dfDict["Data"]["Price of Gold"].diff() / dfDict["Data"]["Price of Gold"]

dfDict["Data"]["Observed Price Elasticity"] = dfDict["Data"]["% Change in Gold Production"]\
                                             / dfDict["Data"]["% Change in Gold Price"] 
dfDict["Data"]['Production MA'] = dfDict["Data"]["Gold Production"].rolling(window=8).mean()
dfDict["Data"]['Price MA'] = dfDict["Data"]["Price of Gold"].rolling(window=8).mean()
dfDict["Data"]["% Change MA Production"] = dfDict["Data"]['Production MA'].diff()\
                                                    / dfDict["Data"]['Production MA']
dfDict["Data"]["% Change MA Price"] = dfDict["Data"]['Price MA'].diff()\
                                                    / dfDict["Data"]['Price MA']

plotValues(dfDict["Data"],["Gold Production","Price of Gold"])

plotValues(dfDict["Data"],["Observed Price Elasticity"])

key1 = "Gold Production"
key2 = "Price of Gold"
scatterPlot(dfDict["Data"], key1,key2,pp,start,end)

key1 = "% Change in Gold Production"
key2 = "% Change in Gold Price"
plotValues(dfDict["Data"],[key1,key2])
scatterPlot(dfDict["Data"], key1,key2,pp,start,end)
key1 = "% Change MA Production"
key2 = "% Change MA Price"
scatterPlot(dfDict["Data"], key1,key2,pp,start,end)

pp.close()