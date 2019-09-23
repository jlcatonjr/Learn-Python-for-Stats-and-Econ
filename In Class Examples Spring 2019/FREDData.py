#quandlFinancePandas.py
# import pandas library
import pandas as pd

#fix update bug fofr datareader
pd.core.common.is_list_like = pd.api.types.is_list_like
#allows pandas to import data (mostly financial)
import pandas_datareader.data as web

# matplotlib is popular visualization library in Python
import matplotlib.pyplot as plt

# this allow you to save images in pdf
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np
#creates date and time recognized by panda datareader
import datetime

def plotDF(df, names,pp, title="", secondary_y=False, logy=False, legend=False, dataType="",
           start=None,end=None):
#    start = df.index[0]
    plt.rcParams['axes.ymargin'] = .01# * df[names].max().max()
    plt.rcParams['axes.xmargin'] = 0
    plt.rcParams.update({'font.size': 25})

    fig, ax1 = plt.subplots(figsize=(24,12))
#    vlinePowell= datetime.datetime(2018, 2, 5)
#    vlineObama = datetime.datetime(2009, 3, 31)
    vlineNixon = datetime.datetime(1971, 8, 15)
    vlineVolcker = datetime.datetime(1979, 8, 6)
    plt.axvline(vlineNixon, color="k",ls="--")  
    plt.text(vlineNixon,.5," End of\n Gold\n Standard" )
    plt.axvline(vlineVolcker, color="k",ls="--")  
    plt.text(vlineVolcker,1," Volcker\n Appointed" )
    
#    plt.axvline(vlineObama,color="b",ls="-")
#    plt.axvline(vlineTrump,color="r",ls="-")
    #    plt.text(vlineObama.year + .5,.9 * df.max().max(),"Obama", fontsize = 24)
#    plt.text(vlineTrump.year + .5,.9 * df.max().max(),"Trump", fontsize = 24)

    #plot data synced to different y-axes
    ls = ["-","--"]
    lns=[]  
    if secondary_y != False:
        ax2 = ax1.twinx()        
    for i in range(len(names)):
        name = names[i]

        if name != secondary_y:
            lns.append(ax1.plot(df[name],ls=ls[i])[0])
            
        
            
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


start = datetime.datetime(1960, 12, 31)
end = datetime.datetime(2019, 12, 31)

data = web.DataReader("DTB3", "fred", start, end).resample("Q").first()
data["CPI"] = web.DataReader("CPIAUCNS", "fred", start, end).resample("Q").first()
data = data.rename(columns={"DTB3":"3 Month Treasury"})
data["GDP Deflator"] = web.DataReader("GDPDEF", "fred", start, end).resample("Q").first()
data["Inflation (CPI)"] = (data["CPI"].diff(4) / data["CPI"]) * 100
data["Inflation (GDP Deflator)"] = (data["GDP Deflator"].diff(4) / data["GDP Deflator"]) * 100
print(data)
pp = PdfPages("Regulation Q Era.pdf")
plotDF(data,["3 Month Treasury", "Inflation (CPI)"], pp)
plotDF(data,["3 Month Treasury", "Inflation (GDP Deflator)"], pp)
