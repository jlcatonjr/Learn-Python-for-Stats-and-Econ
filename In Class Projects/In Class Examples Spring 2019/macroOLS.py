#macroOLS.py
import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like
import pandas_datareader.data as web
import datetime
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
        df[keys].plot.line(figsize=(24,12), legend=False)
        plt.title(key + "\n" + datatype, fontsize=40)
        plt.show()
        plt.close()


def buildSummaryCSV(csvSummary, csvName):    
    #Create a new csv file
    file = open(csvName + ".csv", "w")
    #write results in csv file
    file.write(csvSummary)
    #close CSV
    file.close()
    
start = datetime.datetime(2009, 1, 1)
end = datetime.datetime(2018, 8, 1)
dfDict = {}

dfDict["QData"] = web.DataReader("GDPC1", "fred", start, end).resample("Q").first()
dfDict["QData"] = dfDict["QData"].rename(columns = {"GDPC1":"Real GDP"}) 
dfDict["QData"]["Nominal GDP"] = web.DataReader("GDP", "fred", start, end).resample("Q").first()
dfDict["QData"]["GDP Deflator"] = web.DataReader("GDPDEF", "fred", start, end).resample("Q").first()
dfDict["QData"]["Base Money"] = web.DataReader("AMBNS", "fred",start, end).resample("Q").first() * 1000
dfDict["QData"]["IOER"]  = web.DataReader("IOER", "fred", start, end).resample("Q").first()
dfDict["QData"]["Excess Reserves"] = web.DataReader("EXCSRESNS", "fred", start, end).resample("Q").first()
dfDict["QData"]["Effective Base"] = dfDict["QData"]["Base Money"] - dfDict["QData"]["Excess Reserves"]
dfDict["Logged Data"] = {}
dfDict["Logged First Difference Data"] = {}


#for loop to create logged data and logged first difference data
for key in dfDict["QData"]:
    # create logged data by np.log(dataframe)
    dfDict["Logged Data"][key] = np.log(dfDict["QData"][key])
    # create first difference data by dataframe.diff()
    dfDict["Logged First Difference Data"][key] = dfDict["Logged Data"][key].diff().dropna()


sumStatsDict = {}
sumStatsCats = ["Mean", "Median", "Variance"]

for key1 in dfDict:
    sumStatsDict[key1] = {}
    for key2 in dfDict["QData"]:
        df = dfDict[key1][key2]
        sumStatsDict[key1][key2]={}
        for j in range(len(sumStatsCats)):
            key3 = sumStatsCats[j]
    
            if key3 == "Mean":
                sumStatsDict[key1][key2][key3] = np.mean(df) 
            if key3 == "Median":
                sumStatsDict[key1][key2][key3] = np.median(df)
            if key3 == "Variance":
                sumStatsDict[key1][key2][key3] = np.var(df)


# adjust text size in plots
plt.rcParams.update({'font.size': 24})
# reduce white space in margins to zero
plt.rcParams['axes.ymargin'] = 0
plt.rcParams['axes.xmargin'] = 0

for datatype in dfDict:
    for key in dfDict["QData"]:
        df = dfDict[datatype]
        plotValues(df, key)

# make dataframe out of all Logged First Difference Data 
# drop NAN values
dataFrame = pd.DataFrame(dfDict["Logged First Difference Data"]).dropna()

# create dictionary to hold our Endogenous (Y) Variables and Exogenous (X) variables
regVarDict = {}
regVarDict["Endogenous"] = ["Effective Base"]
regVarDict["Exogenous"] = [["Nominal GDP"], ["Real GDP", "GDP Deflator"],
           ["Excess Reserves", "Base Money"]]

# Use for loops to cycle through different regression
#for endogVar... cycles through endogenous variable
for endogVar in regVarDict["Endogenous"]:
    # for exogVars cycles through different sets of exogenous variables
    for exogVars in regVarDict["Exogenous"]:
        # run regression
        results = OLSRegression(dataFrame, endogVar, exogVars)
        print(results.summary())
        #e xport results to CSV
        buildSummaryCSV(str(results.summary()), str(endogVar)\
                        + "~"+ str(exogVars))
        
