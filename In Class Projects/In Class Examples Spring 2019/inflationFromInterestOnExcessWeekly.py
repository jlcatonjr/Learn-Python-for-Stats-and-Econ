import pandas as pd
pd.core.common.is_list_like = pd.api.types.is_list_like

import pandas_datareader.data as web
import datetime
import matplotlib.pyplot as plt
import numpy as np
import os
import copy
from matplotlib.backends.backend_pdf import PdfPages
from statsmodels.tsa.api import VAR, DynamicVAR


def plotDF(df, names,pp, title="", secondary_y=None, logy=False, legend=False, dataType="",
           start=None,end=None):
#    start = df.index[0]
    plt.rcParams['axes.ymargin'] = .01
    plt.rcParams['axes.xmargin'] = 0
    
    fig, ax1 = plt.subplots(figsize=(24,12))
    vlinePowell= datetime.datetime(2018, 2, 5)
    vlineObama = datetime.datetime(2009, 3, 31)
    vlineTrump = datetime.datetime(2017, 3, 31)
    plt.axvline(vlinePowell, color="k",ls="--")    

    #plot data synced to different y-axes
    lns=[]  
    if secondary_y != False:
        ax2 = ax1.twinx()        
    for i in range(len(names)):
        name = names[i]

        if name != secondary_y:
            lns.append(ax1.plot(df[name])[0])
            
        
            
        else:
##            if "Divisia" in name:
##                lns.append(ax2.plot(df[name], ls="--", linewidth=3)[0])
#            else:
            lns.append(ax2.plot(df[name], ls="-",color="C2")[0])
    
    #Rotate date labels
    ax1.tick_params(axis='x', rotation=90)
    if logy:
        ax1.set_yscale("log")

    labs = [ln.get_label() for ln in lns]
    
    for i in range(len(labs)):
        print(labs[i])
        if labs[i] == secondary_y:
            labs[i] = labs[i] + " (right)"
    plt.rcParams.update({'legend.fontsize': 22,'legend.handlelength': 2})
#    ax1.legend(lns, labs, bbox_to_anchor=(.73 ,1.025 + .05 * len(labs)), loc=2)  
    ax1.legend(lns, labs, bbox_to_anchor=(0, 1.027 + .05 * len(labs)), loc=2)  
#    ax1.legend(lns, labs, bbox_to_anchor=(.64, 1.025 + .05 * len(labs)), loc=2)  
#    df[keys].plot.line(figsize=(24,12), legend=False, secondary_y = keys[0])
#    plt.title(str(keys).replace("[","").replace("]",""), fontsize=40)



#    fig = df[names][start:end].plot.line(logy=logy, secondary_y=secondary_y, legend=legend,figsize=(10,6), color=['k', 'C3','C0'], fontsize=14).get_figure()
#    if any([("Rate" in name) for name in names])  : plt.axhline(0, color="k", ls="--", linewidth=1)
#    plt.xticks(rotation=90)
#    plt.xlabel(df.index.name, fontsize=18)
#    if title == "":
#        if len(names) < 2:
#            plt.title(names[0], fontsize=24)
#    else:
#        plt.title(title)
#    plt.gcf()
    if start == None:start=""
    if end == None: end = ""
    plt.savefig(dataType + " " + str(names[0]) +'.png',bbox_inches="tight")
    plt.show()
    pp.savefig(fig, bbox_inches="tight")
    plt.close()
    
    
def scatterPlot(df, key1,key2,pp,dataType, title=""):
    fig,ax = plt.subplots(figsize=(24,12))
    plt.scatter(x=df[key1], y=df[key2], s = 10**2)
    plt.axhline(0, ls = "--", color="k", linewidth = 1)
    plt.axvline(0, ls="--", color="k", linewidth = 1)
    ax.set_xlabel(key1)
    ax.set_ylabel(key2)
    ax.set_xlim(min(df[key1]) * .98, max(df[key1]) * 1.02)
    ax.set_ylim(min(df[key2]) * .98, max(df[key2]) * 1.02)
    plt.savefig(dataType + " " + str(start).replace(":","") + "-" + str(end).replace(":","")+ " " +
            str(names).replace('[',' ').replace(']',' scatter '+'.png'),bbox_inches="tight")

    plt.show()
    pp.savefig(fig, bbox_inches="tight")
    plt.close()


def buildSummaryCSV(fullPredictResults, csvName, folder):
    try:
        os.mkdir(folder)
    except:
        print(folder, "already exists")
    predictorModelResults= str(fullPredictResults.summary())
    file = open(folder + "\\" + csvName + ".csv" ,"w")
    file.write(predictorModelResults)
    file.close()

plt.rcParams.update({'font.size': 32})

#divisiaAggregates = pd.DataFrame.from_csv("DivisiaAggregates.csv")
datetime.datetime.today()
pp = PdfPages("FedPlots" + str(datetime.datetime.today())[:10] + ".pdf")
start = datetime.datetime(2010, 1, 1)
end = datetime.datetime(2019, 1, 31)
##annual data
dfDict = {}
dfDict["Diff"]={}
###
dfDict["Data"]  = web.DataReader("IOER", "fred", start, end).resample("M").first()
dfDict["Data"]["Excess Reserves"] = web.DataReader("EXCSRESNS", "fred", start, end).resample("M").first()
#dfDict["Diff"] = dfDict["Diff"].rename(columns = {"Real GDP (Logged)":"Real GDP"})
#
#

#
#dfDict["Data"]["Divisia M4 with Treasuries"] = divisiaAggregates["Jan-09":]["Divisia M4 with Treasuries"].values * 10e9
#dfDict["Data"]["Divisia M4 no Treasuries"] = divisiaAggregates["Jan-09":]["Divisia M4 w/o Treasuries"].values * 10e9
#
#
dfDict["Data"]["Base Money"] = web.DataReader("AMBNS", "fred",start, end).resample("M").first()
dfDict["Data"]["Base Money"] = dfDict["Data"]["Base Money"] * 1000
dfDict["Data"]["Base Money (Logged)"] = np.log(dfDict["Data"]["Base Money"])

dfDict["Data"]["M1"] = web.DataReader("M1", "fred",start, end).resample("M").first() * 1000
#dfDict["Data"]["Base Money"] = dfDict["Data"]["Base Money"] * 1000
dfDict["Data"]["M1 (Logged)"] = np.log(dfDict["Data"]["M1"])



dfDict["Data"]["M2"] = web.DataReader("M2", "fred",start, end).resample("M").first() * 1000
#dfDict["Data"]["Base Money"] = dfDict["Data"]["Base Money"] * 1000
dfDict["Data"]["M2 (Logged)"] = np.log(dfDict["Data"]["M2"])



#
dfDict["Data"]["CPI"] = web.DataReader("CPIAUCSL", "fred", start, end).resample("M").first()
dfDict["Data"]["CPI (Logged)"] = np.log(dfDict["Data"]["CPI"])
dfDict["Data"]["CPI Inflation (Annual)"] = ((dfDict["Data"]["CPI (Logged)"].diff() + 1) ** 12 - 1) * 100
dfDict["Data"]["Total Return on ER"] = dfDict["Data"]["IOER"] * dfDict["Data"]["Excess Reserves"]
dfDict["Data"]["% Change in Base from IOER (annual)"] = dfDict["Data"]["Total Return on ER"] / dfDict["Data"]["Base Money"]
dfDict["Data"]["% Change in Effective Base from IOER (annual)"] = dfDict["Data"]["Total Return on ER"] / (dfDict["Data"]["Base Money"] - dfDict["Data"]["Excess Reserves"])
dfDict["Data"]["Effective Base"] = dfDict["Data"]["Base Money"] - dfDict["Data"]["Excess Reserves"]
dfDict["Data"]["Effective Base (Logged)"] = np.log(dfDict["Data"]["Effective Base"])
dfDict["Data"]["Effective Base Annual Growth Rate"] = ((dfDict["Data"]["Effective Base (Logged)"].diff() + 1) ** 12 - 1) * 100
dfDict["Data"]["Base Annual Growth Rate"] = ((dfDict["Data"]["Base Money (Logged)"].diff() + 1) ** 12 - 1) * 100

dfDict["Data"]["% Base in Circulation"] = dfDict["Data"]["Effective Base"]  / dfDict["Data"]["Base Money"] 

#dfDict["Data"]["Real Effective Base"] = dfDict["Data"]["Effective Base"] / dfDict["Data"]["CPI"]
#dfDict["Data"]["Real Effective Base (Logged)"] = np.log(dfDict["Data"]["Real Effective Base"])
#
#dfDict["Data"]["Real Divisia M4 with Treasuries"] = dfDict["Data"]["Divisia M4 with Treasuries"] / dfDict["Data"]["CPI"]
#dfDict["Data"]["Real Divisia M4 with Treasuries (Logged)"] = np.log(dfDict["Data"]["Real Divisia M4 with Treasuries"])
#dfDict["Data"]["Real Divisia M4 no Treasuries"] = dfDict["Data"]["Divisia M4 no Treasuries"] / dfDict["Data"]["CPI"]
#dfDict["Data"]["Real Divisia M4 no Treasuries (Logged)"] = np.log(dfDict["Data"]["Real Divisia M4 no Treasuries"])
#
#dfDict["QData"]["Divisia M4 with Treasuries"] = dfDict["Data"]["Divisia M4 with Treasuries"].resample("Q").first() 
#dfDict["QData"]["Divisia M4 no Treasuries"] = dfDict["Data"]["Divisia M4 no Treasuries"].resample("Q").first() 
#dfDict["QData"]["Divisia M4 with Treasuries (Logged)"] = np.log(dfDict["QData"]["Divisia M4 with Treasuries"])
#dfDict["QData"]["Divisia M4 no Treasuries (Logged)"] = np.log(dfDict["QData"]["Divisia M4 no Treasuries"])
#dfDict["QData"]["Real Divisia M4 with Treasuries"] = dfDict["Data"]["Real Divisia M4 with Treasuries"].resample("Q").first()
#dfDict["QData"]["Real Divisia M4 with Treasuries (Logged)"] = dfDict["Data"]["Real Divisia M4 with Treasuries (Logged)"].resample("Q").first()
#dfDict["QData"]["Real Divisia M4 no Treasuries"] = dfDict["Data"]["Real Divisia M4 no Treasuries"].resample("Q").first()
#dfDict["QData"]["Real Divisia M4 no Treasuries (Logged)"] = dfDict["Data"]["Real Divisia M4 no Treasuries (Logged)"].resample("Q").first()
#dfDict["Diff"]["Divisia M4 with Treasuries"] = dfDict["QData"]["Divisia M4 with Treasuries (Logged)"].diff().dropna()
#dfDict["Diff"]["Divisia M4 no Treasuries"] = dfDict["QData"]["Divisia M4 no Treasuries (Logged)"].diff().dropna()


dfDict["Data"]["Inflation Rate (Annualized)"] = ((np.log(web.DataReader("CPALTT01USM661S", "fred",start, end).resample("M").first()).diff() + 1) ** 12 - 1) * 100
#dfDict["QData"]["CPI"] = dfDict["Data"]["CPI"].resample("Q").first()
#dfDict["QData"]["CPI (Logged)"] = np.log(dfDict["QData"]["CPI"])
#dfDict["QData"]["CPI Inflation (Annual)"] = ((dfDict["QData"]["CPI (Logged)"].diff() + 1) ** 4 - 1) * 100




dfDict["Data"]["Total Fed Assets"] = web.DataReader("WALCL", "fred",start, end).resample("M").first()#).diff() + 1) ** 12 - 1) * 100
dfDict["Data"]["Total Fed Assets (Logged)"] = np.log(dfDict["Data"]["Total Fed Assets"])#).diff() + 1) ** 12 - 1) * 100
dfDict["Data"]["Total Fed Assets (Annualized Rate)"] = ((dfDict["Data"]["Total Fed Assets (Logged)"].diff() + 1) ** 12 - 1) * 100


dfDict["Data"]["Monetary Base Less Assets Held by Fed"] = dfDict["Data"]["Base Money"] - dfDict["Data"]["Total Fed Assets"]
dfDict["Data"]["Base to Assets Ratio"] = dfDict["Data"]["Base Money"] / dfDict["Data"]["Total Fed Assets"]
FV = dfDict["Data"]["Effective Base"][-1]
PV = dfDict["Data"]["Effective Base"][0]
t = (len(dfDict["Data"]) - 1) / 12
n = 12
r = ((FV/PV) ** (1/(n*t)) - 1) * n
dfDict["Data"]["Average Growth Rate of Base"] = pd.DataFrame([r * 100] * len(dfDict["Data"]))
dfDict["Data"]["Required Reserves"] = web.DataReader("REQRESNS", "fred", start, end).resample("M").first()
dfDict["Data"]["Required Reserves (Logged)"] = np.log(dfDict["Data"]["Required Reserves"])


dfDict["Data"]["Dow Jones"] = web.DataReader("DJIA", "fred", start, end).resample("M").first()
dfDict["Data"]["Dow Jones (Logged)"] = np.log(dfDict["Data"]["Dow Jones"])
dfDict["Data"]["Dow Jones Growth Rate (Monthly)"] = dfDict["Data"]["Dow Jones (Logged)"].diff()
dfDict["Data"]["Yen to Dollar Exchange Rate"] = web.DataReader("EXJPUS", "fred", start, end).resample("M").first()
dfDict["Data"]["Dollar to Yen Exchange Rate"] = 1 / dfDict["Data"]["Yen to Dollar Exchange Rate"]
dfDict["Data"]["Dollar Index (Trade Weighted)"] = web.DataReader("DTWEXM", "fred", start, end).resample("M").first()
dfDict["Data"]["Real Dollar Index (Trade Weighted)"] = web.DataReader("TWEXBPA", "fred", start, end).resample("M").first()

#plotSets = {}
dfDict["Data"].index.name= 'Year'

#names = ["Dollar Index (Trade Weighted)","Real Dollar Index (Trade Weighted)"]
#plotDF(dfDict["Data"], names,pp, title="", secondary_y="Real Dollar Index (Trade Weighted)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Yen to Dollar Exchange Rate", "Dollar to Yen Exchange Rate"]
#plotDF(dfDict["Data"], names,pp, title="", secondary_y="Dollar to Yen Exchange Rate", logy=False, legend=True, dataType="",
#           start=start,end=end)
#
names = ["IOER", "% Change in Base from IOER (annual)", "% Change in Effective Base from IOER (annual)", "% Base in Circulation"]
#
plotDF(dfDict["Data"], names,pp, title="", secondary_y="% Base in Circulation", logy=False, legend=True, dataType="",
           start=start,end=end)
#names = ["% Change in Effective Base from IOER (annual)", "% Change in Effective Base", "Inflation Rate"]
#names = ["Inflation Rate (Annualized)", "Effective Base (Annualized Rate)"]
#plotDF(dfDict["Data"], names,pp, title="", secondary_y="Inflation Rate", logy=False, legend=True, dataType="",
#           start=start,end=end)

names = ["Base Money", "Effective Base", "% Base in Circulation"]
plotDF(dfDict["Data"], names,pp, title="", secondary_y="% Base in Circulation", logy=False, legend=True, dataType="",
           start=start,end=end)

names = ["Base Money", "Total Fed Assets", "Base to Assets Ratio"]
plotDF(dfDict["Data"], names,pp, title="", secondary_y="Base to Assets Ratio", logy=False, legend=True, dataType="",
           start=start,end=end)

names = ["IOER", "% Base in Circulation"]
plotDF(dfDict["Data"], names,pp, title="", secondary_y="% Base in Circulation", logy=False, legend=True, dataType="",
           start=start,end=end)
names = ["IOER", "Effective Base Annual Growth Rate"]
plotDF(dfDict["Data"], names,pp, title="", secondary_y="IOER", logy=False, legend=True, dataType="",
           start=start,end=end)

names = ["Base Annual Growth Rate", "Effective Base Annual Growth Rate"]
plotDF(dfDict["Data"], names,pp, title="", secondary_y=False, logy=False, legend=True, dataType="",
           start=start,end=end)
#names = ["Inflation Rate (Annualized)", "Effective Base (Annualized Rate)"]
#plotDF(dfDict["Data"], names,pp, title="", secondary_y="Effective Base (Annualized Rate)", logy=False, legend=True, dataType="",
#           start=start,end=end)

#names = ["Real Effective Base (Logged)", "IOER"]
#plotDF(dfDict["Data"], names,pp, title="", secondary_y="IOER", logy=False, legend=True, dataType="",
#           start=start,end=end)
#
#names = ["Effective Base Velocity", "Real GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="IOER", logy=False, legend=True, dataType="",
#           start=start,end=end)


#names = ["Real Divisia M4 with Treasuries", "IOER"]
#plotDF(dfDict["Data"], names,pp, title="", secondary_y="IOER", logy=False, legend=True, dataType="",
#           start=start,end=end)


#names = ["Base Money (Logged)", "GDP Deflator (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="GDP Deflator (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Base Money", "GDP Deflator"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Base Money (Logged)", "Real GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Real GDP(Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Base Money", "Real GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Base Money (Logged)", "Nominal GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Nominal GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Base Money", "Nominal GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Effective Base (Logged)", "GDP Deflator (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="GDP Deflator (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Effective Base", "GDP Deflator"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Effective Base (Logged)", "Real GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Real GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Effective Base", "Real GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Effective Base (Logged)", "Nominal GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Nominal GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Effective Base", "Nominal GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["M1 (Logged)", "GDP Deflator (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="GDP Deflator (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["M1", "GDP Deflator"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["M1 (Logged)", "Real GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Real GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["M1", "Real GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["M1 (Logged)", "Nominal GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Nominal GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["M1", "Nominal GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["M2 (Logged)", "GDP Deflator (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="GDP Deflator (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["M2", "GDP Deflator"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["M2 (Logged)", "Real GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Real GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["M2", "Real GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["M2 (Logged)", "Nominal GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Nominal GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["M2", "Nominal GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Divisia M4 with Treasuries (Logged)", "GDP Deflator (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="GDP Deflator (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Divisia M4 with Treasuries", "GDP Deflator"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Divisia M4 with Treasuries (Logged)", "Real GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Real GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Divisia M4 with Treasuries", "Real GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Divisia M4 with Treasuries (Logged)", "Nominal GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Nominal GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Divisia M4 with Treasuries", "Nominal GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Divisia M4 no Treasuries (Logged)", "GDP Deflator (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="GDP Deflator (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Divisia M4 no Treasuries", "GDP Deflator"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Divisia M4 no Treasuries (Logged)", "Real GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Real GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#names = ["Divisia M4 no Treasuries", "Real GDP"]
#dataType = "Diff"
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
#
#names = ["Divisia M4 no Treasuries (Logged)", "Nominal GDP (Logged)"]
#plotDF(dfDict["QData"], names,pp, title="", secondary_y="Nominal GDP (Logged)", logy=False, legend=True, dataType="",
#           start=start,end=end)
#dataType = "Diff"
#names = ["Divisia M4 no Treasuries", "Nominal GDP"]
##scatterPlot(dfDict[dataType], key1=names[0],key2=names[1],pp=pp,dataType=dataType)
#
##names = ["Required Reserves (Logged)", "Dow Jones (Logged)"]
##plotDF(dfDict["Data"], names,pp, title="", secondary_y="Dow Jones (Logged)", logy=False, legend=True, dataType="",
##           start=start,end=end)
#
#CPIGrowth = (dfDict["Data"]["CPI"][-1] - dfDict["Data"]["CPI"][0])/dfDict["Data"]["CPI"][0]
#BaseGrowth = (dfDict["Data"]["Base Money"][-1] - dfDict["Data"]["Base Money"][0])/dfDict["Data"]["Base Money"][0]
#EffectiveBaseGrowth = (dfDict["Data"]["Effective Base"][-1] - dfDict["Data"]["Effective Base"][0])/dfDict["Data"]["Effective Base"][0]
#M1Growth = (dfDict["Data"]["M1"][-2] - dfDict["Data"]["M1"][0])/dfDict["Data"]["M1"][0]
#M2Growth = (dfDict["Data"]["M2"][-2] - dfDict["Data"]["M2"][0])/dfDict["Data"]["M2"][0]
#CommercialLiabilityGrowth = (dfDict["Data"]["Total Commercial Liabilities"][-1] - dfDict["Data"]["Total Commercial Liabilities"][0])/dfDict["Data"]["Total Commercial Liabilities"][0]
#RealGDPGrowth = (dfDict["QData"]["Real GDP"][-1] - dfDict["QData"]["Real GDP"][0])/dfDict["QData"]["Real GDP"][0]
#GDPDeflatorGrowth = (dfDict["QData"]["GDP Deflator"][-1] - dfDict["QData"]["GDP Deflator"][0])/dfDict["QData"]["GDP Deflator"][0]
#NGDPGrowth = (dfDict["QData"]["Nominal GDP"][-1] - dfDict["QData"]["Nominal GDP"][0])/dfDict["QData"]["Nominal GDP"][0]
#DM4WTGrowth = (dfDict["Data"]["Divisia M4 with Treasuries"][-1] - dfDict["Data"]["Divisia M4 with Treasuries"][0])/ dfDict["Data"]["Divisia M4 with Treasuries"][0]
#DM4NTGrowth = (dfDict["Data"]["Divisia M4 no Treasuries"][-1] - dfDict["Data"]["Divisia M4 no Treasuries"][0])/ dfDict["Data"]["Divisia M4 no Treasuries"][0]
#RequiredReservesToCommercialLiabilitiesGrowth = (dfDict["Data"]["Required Reserves to Total Commercial Liabilities"][-1] -
#                                                   dfDict["Data"]["Required Reserves to Total Commercial Liabilities"][0]) / dfDict["Data"]["Required Reserves to Total Commercial Liabilities"][0]
#DowJonesGrowth = (dfDict["Data"]["Dow Jones"][-1] - dfDict["Data"]["Dow Jones"][0]) / dfDict["Data"]["Dow Jones"][0]
#SP500Growth = (dfDict["Data"]["S&P 500"][-1] - dfDict["Data"]["S&P 500"][0]) / dfDict["Data"]["S&P 500"][0]
#
#print("CPI Growth:", CPIGrowth)
#print("Growth of Base:", BaseGrowth)
#print("Growth of Effective Base:", EffectiveBaseGrowth)
#print("Growth of M1:", M1Growth)
#print("Growth of M2:", M2Growth)
#print("Divisia M4 with Treasuries Growth:", DM4WTGrowth)
#print("Divisia M4 without Treasuries Growth:", DM4NTGrowth)
#
#print("Growth of Commercial Liabilities:", CommercialLiabilityGrowth)
#print("RealGDPGrowth:", RealGDPGrowth)
#print("GDP Deflator Growth", GDPDeflatorGrowth)
#print("NGDP Growth", NGDPGrowth)
#print("Dow Jones Growth", DowJonesGrowth)
#print("S&P 500 Growth", SP500Growth)
#print("Growth of Required Reserves to Commercial Liabilities:", RequiredReservesToCommercialLiabilitiesGrowth)
#print("Effective Base Growth - NGDP Growth", EffectiveBaseGrowth - NGDPGrowth)
#print("CommercialLiabilityGrowth - NGDP Growth", CommercialLiabilityGrowth- NGDPGrowth)
#print("Required Reserve Ratio Growth:", RequiredReservesToCommercialLiabilitiesGrowth)
#print("CommercialLiabilityGrowth - CPI Growth - Real GDP Growth", CommercialLiabilityGrowth - CPIGrowth - RealGDPGrowth)
#print("CommercialLiabilityGrowth - NGDP Growth - Required Reserve Ratio Growth", CommercialLiabilityGrowth - NGDPGrowth - RequiredReservesToCommercialLiabilitiesGrowth)
#print("Effective Base Growth - NGDP Growth - Required Reserve Ratio Growth", EffectiveBaseGrowth - NGDPGrowth - RequiredReservesToCommercialLiabilitiesGrowth)
#print("Effective Base Growth - Dow Jones - Required Reserve Ratio Growth", EffectiveBaseGrowth - DowJonesGrowth- RequiredReservesToCommercialLiabilitiesGrowth)
#
#print("Base Growth - NGDP Growth", BaseGrowth - NGDPGrowth)
#print("Effective Base Growth - NGDP Growth", EffectiveBaseGrowth - NGDPGrowth)
#print("M1 Growth - NGDP Growth", M1Growth - NGDPGrowth)
#print("M2 Growth - NGDP Growth", M2Growth - NGDPGrowth)
#print("Divisia M4 with Treasuries Growth - NGDP Growth:", DM4WTGrowth - NGDPGrowth)
#print("Divisia M4 without Treasuries Growth - NGDP Growth:", DM4NTGrowth - NGDPGrowth)
##print("Divisia M4 with Treasuries Growth - NGDP Growth - Required Reserve Ratio Growth", DM4WTGrowth - NGDPGrowth - RequiredReservesToCommercialLiabilitiesGrowth)
#
##PV = FV /(1+r/n)**(n*t)
##PV/FV =1/ (1+r/n)**(n*t)
##FV/PV = (1+r/n)**(n*t)
##(FV/PV) ** (1/(n*t)) = (1 + r/n)
##(FV/PV) ** 1/(n*t) - 1 = r/n
#
#
#print(r)
pp.close()
#names = {}
#names[0] = ["Required Reserves to Total Commercial Liabilities (Quarterly Change)", "Dow Jones Growth Rate (Quarterly)"]
#names[1] = ["Required Reserves to Total Commercial Liabilities", "Dow Jones (Logged)"]
#
#names[2] = ["Effective Base (Logged)", "Required Reserves to Total Commercial Liabilities", "GDP Deflator (Logged)"]
#names[3] = ["Effective Base (Logged)", "Required Reserves to Total Commercial Liabilities", "CPI (Logged)"]
#lags = 4
#folder = "VAR Regressions"
#for key in names:
#    var = VAR(dfDict["QData"][names[key]].dropna())
#    for i in range(1,lags+1):
#        res = var.fit(i)
#        print("VAR with " + str(i) + " lags")
##        print(res.summary())
#        fileName = str(names[key]).replace("[","").replace("]","") + " " + \
#            str(i) + " Lags"
#        buildSummaryCSV(res, fileName, folder)