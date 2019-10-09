#econFreedomRegression.py
import pandas as pd
import copy
import numpy as np
from scipy.stats import t
import matplotlib.pyplot as plt
from stats import Stats
import sys

class Regression:
    def __init__(self):
        self.stats = Stats()
        self.all_regressions = {}
        self.indicator_names = []
        
    def regress(self, reg_name, data, y_name, X_names, min_val = 0,
                max_val = None, constant = True):
        self.reg_name = reg_name
        self.all_regressions[self.reg_name] = {}
        self.min_val = min_val
        if max_val != None:
            self.max_val = max_val
        else:
            self.max_val = len(data)
                    
        # self.data is a copy of data, avoid changing original dataframe
        self.y_name = y_name
        self.X_names = copy.copy(X_names)
        self.data = copy.copy(data)
        if constant:
            self.add_constant()
        self.build_matrices()
        self.estimate_betas_and_yhat()
        self.calculate_regression_stats()
        self.X_names = self.X_names        
        self.save_reg_stats()
        
    def panel_regression(self, reg_name, data, y_name, X_names, min_val = 0,
                         max_val = None, entity = False, time = False, 
                         constant = True, ):
        if (entity and time) or (not entity and not time): 
            print("Choose time OR entity for panel regression. Cannot choose\
                  both or neither option.")
            sys.exit()
        #identify which index column holds dates, which holds entities
        for i in range(len(data.index.levels)):
            if isinstance(data.index.levels[i], pd.DatetimeIndex):
                date_level = i
                date_index_name = data.index.names[date_level]
            else:
                entity_level = i
                entity_index_name = data.index.names[entity_level]
        #save name of selected index 
        index_name = entity_index_name if entity else date_index_name 
        #reduce list to unique elements and sort
        self.indicator_names = list(set(data.index.get_level_values(index_name)))
        self.indicator_names= sorted(self.indicator_names)
        self.indicator_names.pop()
        #
        for indicator in self.indicator_names:
            self.create_indicator_variable(data, indicator, index_name,
                                           [indicator])
        X_and_indicator_names = X_names + self.indicator_names
                        
        self.regress(reg_name = reg_name, data = data, y_name = y_name, 
                X_names = X_and_indicator_names, min_val = min_val, 
                max_val = max_val, constant = constant)
        self.data = self.data[self.X_names]
        self.estimates = self.estimates.ix[self.X_names]
            
    def create_indicator_variable(self, data, indicator_name, index_name, 
                                  target_index_list):
        # Prepare column with name of indicator variable
        data[indicator_name] = 0
        # for each index whose name matches an entry in target_index_list
        # a value of 1 will be recorded
        for index in target_index_list:
            data[indicator_name].loc[(data.index.get_level_values(\
                index_name)== index)] = 1

    def add_constant(self):
        self.data["Constant"] = 1
        self.X_names.append("Constant")
    
    def build_matrices(self):
        # Transform dataframes to matrices
        self.y = np.matrix(self.data[self.y_name]\
                           [self.min_val:self.max_val])
        # create a k x n nested list containg vectors for each xi
        self.X = self.data[self.X_names].values
        # create X Array
        self.X = np.matrix(self.X)
        self.X_transpose = np.matrix(self.X.getT())
        
        # (X'X)^-1
        X_transp_X = np.matmul(self.X_transpose, self.X)
        self.X_transp_X_inv = X_transp_X.getI()
        #X'y
        self.X_transp_y = np.matmul(self.X_transpose, self.y)
    
    def estimate_betas_and_yhat(self):
        # betas = (X'X)^-1 * X'y
        self.betas = np.matmul(self.X_transp_X_inv, self.X_transp_y)
        # y-hat = X * betas
        self.y_hat = np.matmul(self.X, self.betas)
        # Create a column that holds y_hat values
        self.data[self.y_name[0] + " estimator"] = [i.item(0) for i in self.y_hat]
        # create a table that holds the estimated coefficient
        # this will aslo be used to store SEs, t-stats, and p-values
        self.estimates = pd.DataFrame(self.betas, index = self.X_names,
                         columns = ["Coefficient"])
        # identify y variable in index
        self.estimates.index.name ="y = " + self.y_name[0]

    def remove_indicator_names(self):
        #save X_names without indicator variables in case of panel regression
        for name in self.indicator_names:
            try:
                self.X_names.remove(name)
            except:
                print(name, "not in list")

    
    def calculate_regression_stats(self):
        self.sum_square_stats()
        self.calculate_degrees_of_freedom()
        self.calculate_estimator_variance()
        self.calculate_covariance_matrix()
        # done using indicator variables
        self.remove_indicator_names()
        self.calculate_t_p_error_stats()
        self.calculate_MSE()
        self.calculate_rsquared()
        self.caculate_adjusted_rsquared()
        self.calculate_fstat()
        self.build_stats_DF()
        self.save_reg_stats()
    def sum_square_stats(self):
        ssr_list = []
        sse_list = []
        sst_list = []
        mean_y = self.stats.mean(self.y).item(0)
        for i in range(len(self.y)):
            yhat_i = self.y_hat[i]
            y_i =self.y[i]
            ssr_list.append((yhat_i - mean_y) ** 2)
            sse_list.append((y_i - yhat_i) ** 2)
            sst_list.append((y_i - mean_y) ** 2)
        self.ssr = self.stats.total(ssr_list).item(0)
        self.sst = self.stats.total(sst_list).item(0)
        self.sse = self.stats.total(sse_list).item(0)
        
    def calculate_degrees_of_freedom(self):
        # Degrees of freedom compares the number of observations to the number
        # of variables ued to form prediction
        self.lost_degrees_of_freedom = len(self.estimates)
        # DoF = num_obs - num_X_variables
        self.degrees_of_freedom = (self.max_val + 1 - self.min_val) \
                            - self.lost_degrees_of_freedom
    
    def calculate_estimator_variance(self):
        # estimator variance is the sse normalized by the degrees of freedom
        # thus, there is a tradeoff between estimator variance and degrees of
        # freedom
        self.estimator_variance = self.sse / self.degrees_of_freedom
    
    def calculate_covariance_matrix(self):
        # Covariance matrix will be used to estimate standard errors for each 
        # coefficient
        # est_var * (X'X)^-1 is the covariance matrix
        self.cov_matrix = copy.copy(self.X_transp_X_inv)
        if self.estimator_variance != None:
            self.cov_matrix = float(self.estimator_variance) * self.cov_matrix
        self.cov_matrix = pd.DataFrame(self.cov_matrix,
                                       columns = self.X_names,
                                       index = self.X_names)
    
    def calculate_t_p_error_stats(self):
        est = ["SE", "t-stats", "p-value", "p-rating"]
        rating_dict = {.001: "***",
                       .01: "**",
                       .05: "*"}
        results = self.estimates
        for name in est:
            results[name] = np.nan
            for var in self.X_names:
                if name == "SE":
                    # SE of coefficient is found in the diagonal of cov_matrix
                    results.ix[var][name] = \
                    self.cov_matrix[var][var] ** (1/2)
                if name == "t-stats":
                    # tstat = Coef / SE
                    results.ix[var][name] = \
                    results["Coefficient"][var] / results["SE"][var]
                if name == "p-value":
                    # p-values is estimatd from location within a 
                    # distribution implied by the t-stat
                    results.ix[var][name] = round(t.sf(\
                              np.abs(results.ix[var]["t-stats"]),
                                     self.degrees_of_freedom + 1) * 2, 5)
                if name == "p-rating":
                    for val in rating_dict:
                        if results.ix[var]["p-value"] < val:
                            results[name][var] = rating_dict[val]
                            break 
                        results[name][var]= ""
                        
    def calculate_MSE(self):
        self.mse = self.estimator_variance ** (1/2)
    
    def calculate_rsquared (self):
        self.r_sq = self.ssr / self.sst
    
    def caculate_adjusted_rsquared(self):
        n = len(self.y_hat)
        k = len(self.X_names) if "Constant" not in self.X_names \
            else len(self.X_names) - 1
        self.adjusted_r_sq = (self.ssr/(n - k)) / (self.sst / (n - 1))
    
    def calculate_fstat(self):
        self.f_stat = ((self.sst - self.sse) / (self.lost_degrees_of_freedom \
                       -1)) / self.estimator_variance

    def calculate_generalized_fstat(self, restricted_reg_name, 
                                    unrestricted_reg_name):
        r_reg = self.all_regressions[restricted_reg_name]
        r_sse = r_reg["SSE"]
        r_k = len(r_reg["X_names"]) 
        u_reg = self.all_regressions[unrestricted_reg_name]
        u_sse = u_reg["SSE"]
        u_k = len(u_reg["X_names"]) 
        if (len(r_reg["data"]) == len(u_reg["data"])): n = len(r_reg["data"]) 
        lost_dof = (u_k - r_k)
        fstat = ((r_sse - u_sse) / lost_dof) / (u_sse / n - u_k)
        return fstat
                        
    def build_stats_DF(self):
        self.stats_dict = {"r**2":[self.r_sq],
                           "adjusted r**2":[self.adjusted_r_sq],
                           "f-stat":[self.f_stat],
                           "Est Var":[self.estimator_variance],
                           "MSE":[self.mse],
                           "SSE":[self.sse],
                           "SSR":[self.ssr],
                           "SST":[self.sst]
                           }
        self.stats_DF = pd.DataFrame(self.stats_dict)
        self.stats_DF = self.stats_DF.rename(index={0:"Estimation Statistics"})
        self.stats_DF = self.stats_DF.T        
           
    def save_reg_stats(self):
        reg_name = copy.copy(self.reg_name)
        self.all_regressions[reg_name] = \
                        {key:self.stats_dict[key][0] for key in self.stats_dict}
        self.all_regressions[reg_name]["estimates"] = \
                                    copy.copy(self.estimates.ix[self.X_names])
        self.all_regressions[reg_name]["cov_matrix"] = \
                                    copy.copy(self.cov_matrix)
        self.all_regressions[reg_name]["degrees_of_freedom"] = \
                                    copy.copy(self.degrees_of_freedom)
        self.all_regressions[reg_name]["lost_degrees_of_freedom"]=\
                                    copy.copy(self.lost_degrees_of_freedom)
        self.all_regressions[reg_name]["estimator_variance"] =\
                                    copy.copy(self.estimator_variance)
        self.all_regressions[reg_name]["MSE"] = copy.copy(self.mse)
        self.all_regressions[reg_name]["data"] = \
                                    copy.copy(self.data[self.X_names])
        self.all_regressions[reg_name]["y_name"] = copy.copy(self.y_name)
        self.all_regressions[reg_name]["X_names"] = \
                                    copy.copy(self.X_names)
        self.all_regressions[reg_name]["data"]\
                                    [self.y_name[0] + " estimator"] = self.y_hat
        
        
    def plot_scatter_with_estimator(self, data, x_vars, y, figsize = (12,8), 
                                    fontsize = 19, s = 10, y_label1 = "Estimate",
                                    y_label2 = "Observation", estimate_color = "r",
                                    legend_loc = "upper left", bbox = (0, 1.17)):
        # set default font size
        plt.rcParams.update({'font.size': fontsize})
        # use a for loop to call each exogenous variable
        for x in x_vars:
            # prepare a figure that will plot predictor. 
            #We will use ax to specify that the plots are in the same figure
            fig, ax = plt.subplots(figsize = figsize)
            # labels will be in a legend
    #        y_label1 = "Estimate"
    #        y_label2 = "Observation"
            # plot the estimated value
            data.plot.scatter(x = x, y = y[0] + " estimator", ax = ax, 
                              c = estimate_color, s = s, label = y_label1, 
                              legend = False)
            # erase the y-axis label to sho that "estimator is not present
            # the y-label will reappear when the observations are plotted
            plt.ylabel("")
            data.plot.scatter(x = x, y = y, ax = ax, s = s, label = y_label2,
                             legend = False)
            # call the legend, place atop the image on the left
            # bbox_to_anchor used to specify exact placement of label
            plt.legend(loc = legend_loc, labels = [y_label1, y_label2],
                       bbox_to_anchor = bbox)
            # remove lines marking units on the axis
            ax.xaxis.set_ticks_position('none')
            ax.yaxis.set_ticks_position('none')
            plt.show()
            plt.close()
