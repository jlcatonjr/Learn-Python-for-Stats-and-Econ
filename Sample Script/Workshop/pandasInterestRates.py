#pandasInterestRates.py
import pandas as pd
import matplotlib.pyplot as plt

# .set_index("DATE") makes the DATE column the index 
data = pd.read_excel("interestRates.xlsx", parse_dates = True).set_index("DATE")

for key in data:
  # transform each column of data to numeric values, errors are converted to nan
    data[key] = pd.to_numeric(data[key], errors="coerce")
    
# Make column names readable
data = data.rename(columns={"DGS30":"30 Yr Tr Rate", "DGS10":"10 Yr Tr Rate", "DGS1MO": "1 Mo Tr Rate"})

# increase text size for plots
plt.rcParams.update({'font.size': 32})
# remove margins
plt.rcParams['axes.ymargin'] = 0
plt.rcParams['axes.xmargin'] = 0
# plot figure, figsize changes size of the plot
data.plot(figsize = (24,12))
# set title
plt.title("Interest Rates")
# show figure
plt.show()
# close figures
plt.close()