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

#creates date and time recognized by panda datareader
import datetime

#initiate pdf for storing visualizations
pp = PdfPages("stockPlots.pdf")

#save start and end dates in variables 
start = datetime.datetime(2005, 1, 1)
end = datetime.datetime(2018, 9, 18)

#stock symbols to be passed in for loop
stocks = ["MSFT", "AAPL","MCD","AMZN", "KO", "PEP"]

# dictionary that holds measures to be plotted
plotList = {}
plotList[0] = ["Open","High", "Low", "Close"]
plotList[1] = ["Volume"]
plotList[2] = ["SplitRatio"]

#dictionary to hold and categorize data by name
stockData = {}

# use for loop to retrieve data and plot each individual stock
for stock in stocks:    
    
    #identify which stock is being processed
    print(stock)
    
    #use pandas_datareader to retrieve data with quandl
    #dataframe saved as data
    data = web.DataReader('WIKI/' + stock, 'quandl', start, end)
    
    #save data frame as csv
    data.to_csv(stock + ".csv")
    
    #plot each set of indicators
    for key in plotList:  
        names = plotList[key]
        print(names)
        
        #plot data and save as "fig"; indicate linewidth, appearance of legend,
        #   and logging of the yaxis
        fig = data[names].plot.line(linewidth = 1, legend = True, logy = True).get_figure()        
       
        # Add stock symbol as title
        plt.title(stock)
        #makes sure format is correct
        plt.tight_layout()
        #save figure in pdf
        pp.savefig(fig, bbox_inches = 'tight')
        
    stockData[stock] = data

#close PDF so that it can be accessed by user
pp.close()