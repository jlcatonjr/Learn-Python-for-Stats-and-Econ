#econFreedomRegression.py
import pandas as pd
import regression
import statsmodels.api as sm
import matplotlib.pyplot as plt

def plot_scatter_with_estimator(data, x_vars, y):
    #set default font size
    plt.rcParams.update({'font.size': 19})
    # use a for loop to call each exogenous variable
    for x in x_vars:
        # prepare a figure that the predictor. We will use ax to specify that
        # the plots are in the same figure
        fig, ax = plt.subplots(figsize = (12,8))
        # labels will be in a legend that specific
        y_label1 = "Estimate"
        y_label2 = "Observation"
        # plot the estimated value
        reg.data.plot.scatter(x = x, y = y + " estimator", ax = ax, c = "r", 
                              s = 10, label = y_label1, legend = False)
        # erase the y-axis label to so that "estimator" is not present
        # the y-label will reappear when the observations are plotted
        plt.ylabel("")
        reg.data.plot.scatter(x = x, y = y, ax=ax, s = 10, label = y_label2, 
                              legend = False)
        # call the legend, place atop the image on the left 
        # bbox_to_anchor used to specif exact placement of label
        plt.legend(loc = "upper left", labels = [y_label1, y_label2], 
                   bbox_to_anchor = (0,1.17))
        # remove lines marking units on the axis
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        plt.show()
        plt.close()

data = pd.read_csv("cleanedEconFreedomData.csv", index_col = ["Country Name"])
reg = regression.Regression()
print(regression)

y_var = "GDP per Capita (PPP)"
x_vars = ["Gov't Expenditure % of GDP ",
           "2017 Score"]

reg.regress("Economic Freedom and GDP", data, y_var, x_vars)

y = data[y_var]
X = data[x_vars]
X["Constant"] = 1
results = sm.OLS(y, X).fit()

plot_scatter_with_estimator(data,x_vars, y_var)

