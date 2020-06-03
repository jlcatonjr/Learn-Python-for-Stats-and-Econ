#econFreedomRegression
import pandas as pd
from regression import Regression
import statsmodels.api as sm
import matplotlib.pyplot as plt

def plot_scatter_with_estimator(data, x_vars, y_var):
    # set default font size
    plt.rcParams.update({"font.size": 19})
    # use a for loop to call each exogenous variable
    y = y_var[0]
    for x in x_vars:
        # prepare a figure with the predictor. We will use ax to specify that
        # the plots are in the same figure
        fig, ax = plt.subplots(figsize = (12, 8))
        # labels will be in a legend
        y_label1 = "Estimate"
        y_label2 = "Observation"
        # plot the estimated value
        data.plot.scatter(x = x, y = y + " estimator", ax = ax, c = "r",
                          s = 10, label = y_label1, legend = False)
        # erase the y-axis label so that "estimator" is not present
        # the y-label will reappear when the observations are plotted
        plt.ylabel("")
        data.plot.scatter(x = x, y = y, ax = ax, s = 10, label = y_label2,
                          legend = False)
        # call teh legend, place atop the image on the left
        # bbox_to_anchor used to specify exact placement of label
        plt.legend(loc = "upper left", labels = [y_label1, y_label2], 
                   bbox_to_anchor = (0, 1.17))
        # remove lines marking units on the axis
        ax.xaxis.set_ticks_position('none')
        ax.yaxis.set_ticks_position('none')
        plt.show()
        plt.close()

data = pd.read_csv("cleanedEconFreedomData.csv")
reg = Regression()

y_var = ["GDP per Capita (PPP)"]
x_vars = ["Judical Effectiveness", "Property Rights",
          "Fiscal Health", "Investment Freedom ", "Financial Freedom", 
          "Inflation (%)", "Public Debt (% of GDP)"]
reg.OLS("GDP Per Capita Restricted", data, y_var, x_vars)
plot_scatter_with_estimator(reg.data, x_vars, y_var)

x_vars_unrestricted = x_vars
x_vars_restricted = ["Judical Effectiveness", "Property Rights"]
reg.OLS("GDP Per Capita Restricted", data, y_var, x_vars_restricted)
reg.OLS("GDP Per Capita Unrestricted", data, y_var, x_vars_unrestricted)

joint_f_test = reg.joint_f_test("GDP Per Capita Unrestricted", 
                                "GDP Per Capita Restricted")
joint_f_test.to_csv("Joint F_test; y = " + reg.y_name[0] + "; " +\
                    joint_f_test.index.name + ".csv")