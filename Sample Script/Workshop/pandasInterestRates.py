#pandasInterestRates.py
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# create new pdf format: PdfPages(filename)
#pp = PdfPages("interestRates.pdf")
# .set_index("DATE") makes the DATE column the index 
data = pd.read_excel("interestRates.xlsx", parse_dates = True).set_index("DATE")
lags = 4

for key in data:
  # transform each column of data to numeric values, errors are converted to nan
    data[key] = pd.to_numeric(data[key], errors="coerce")
    for lag in range(1, lags + 1):
        data[key + " lag " + str(lag)] = data[key].shift(lag)
## Make column names readable
#data = data.rename(columns={"DGS30":"30 Yr Tr Rate", "DGS10":"10 Yr Tr Rate", 
#                            "DGS1MO": "1 Mo Tr Rate"})
#
## increase text size for plots
#plt.rcParams.update({'font.size': 20})
#
## create figure to store plot, ax will be usd to identify that the plot is to
## be in this figure
#fig, ax = plt.subplots()
#
## Create different types of lines to cycle through
#ls = ["-", "--", ":"]
#i = 0
#
#
#for key in data:
#    style = ls[i]
#    # plot figure, figsize changes size of the plot
#    data[key].plot(linestyle = style, linewidth = 1, figsize = (24,12), ax = ax)
#    i += 1
#plt.xticks(rotation = 60)
#plt.legend(fontsize = 20)
#plt.rcParams["axes.xmargin"] = 0
#plt.rcParams["axes.ymargin"] = 0
#ax.xaxis.set_ticks_position('none') 
## set title
#plt.title("Interest Rates", fontsize = 26)
#plt.show()
#pp.savefig(fig, bbox_inches = "tight")
#plt.close()
#
#for key in data:
#    fig, ax = plt.subplots()
#    data[key].plot(ax = ax)
#    plt.show()
#    pp.savefig(fig)
#    plt.close()
#pp.close()