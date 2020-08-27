import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import copy
import statsmodels.api as sm
from linearmodels import PanelOLS
from matplotlib.backends.backend_pdf import PdfPages

dataByCounty = pd.DataFrame.from_csv("schoolDataRealExpenditures.csv",
                                     index_col = ["County", "Year"],
                                     parse_dates=False)
dataByCounty = dataByCounty[dataByCounty.index.get_level_values("Year") > 1999]
dataByCounty = dataByCounty[dataByCounty.index.get_level_values("Year") < 2017]
dataByCounty = dataByCounty.apply(pd.to_numeric, errors='coerce')


county_index = dataByCounty.index.get_level_values('County')
county_index = set(county_index)
county_index = sorted(list(county_index))
#
# list of different y variables to be estimated
endog = ["Average ACT composite scores",
         "Average daily membership of public schools",
         "Four-year high school cohort graduation rate (percent)",
         "All Four Subject Areas (percent)"]

# list of X variables to explain each y variable
exog = ["Capital Projects (per pupil)",
        "Salaries and Benefits for Instructors (per pupil)"]
pp = PdfPages("NDSchoolRegVis.pdf")
for endogName in endog:
    y = dataByCounty[endogName]
    
    # select X data
    X = dataByCounty[exog]
    exogConst = copy.deepcopy(exog)
    exogConst.append("const")
    X = sm.add_constant(X)
    
    #prepare regression
    mod = PanelOLS(y, X, entity_effects = True, time_effects = False)
    #fit line // generate results
    res = mod.fit(cov_type = "clustered", cluster_entity = True,
                  cluster_time = False)
    
    summary = res.summary
    print(summary)
    for county in county_index:
        try:
                
            # visualize predictor against observation
            fig, ax = plt.subplots(figsize = (12, 8))
            # prepare data for visualization
            county_data = y[y.index.get_level_values("County") == county]
            county_data = county_data.dropna()
            county_data = county_data.reset_index().set_index("Year")

            county_predict = res.predict()[res.predict().\
                                      index.get_level_values("County") == county]
            county_predict = county_predict.dropna()
            county_predict = county_predict.reset_index().set_index("Year")

            # plot data
            county_data.plot.line(ax = ax, legend = False)
            county_predict.plot.line(ax=ax, legend = False)
            plt.title(county, fontsize = 28)
            plt.legend()
            plt.show()
            pp.savefig(fig)
            plt.close()
        except:
            print("Something didn't work for", county, 
                  "you better check it out...")
            
pp.close()