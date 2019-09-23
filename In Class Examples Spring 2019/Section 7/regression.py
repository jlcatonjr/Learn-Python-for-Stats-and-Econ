#regression.py
import pandas as pd
import copy
from stats import *
import numpy as np
from scipy.stats import t

class Regression:
    def __init__(self):
        self.stats = Stats()

    def regress(self, reg_name, data, y_name, beta_names, min_value = 0,
                max_val = None, constant = True):
        self.min_val =  0
        if max_val != None:
            self.max_val = max_val
        else:
            self.max_val = len(data)
        self.reg_name = reg_name
        self.y_name = y_name
        self.beta_names = copy.copy(beta_names)
        self.data = copy.copy(data)
        if constant:
            self.add_constant()
        self.build_matrices()
        self.estimate_betas_and_yhat()
        self.calculate_regression_stats()
        self.build_stats_DF()
        
    def add_constant(self):
        self.data["Constant"] = 1
        self.beta_names.append("Constant")
    
    def build_matrices(self):
        # Transform dataframes to matrices
        self.y = np.matrix(self.data[self.y_name]\
                           [self.min_val:self.max_val]).getT()
        # create a k X n nested list containing vectors for each xi
        self.X = self.data[self.beta_names].values
        # transform the nested list into a matrix
        self.X = np.matrix(self.X)
        # create standard array of X values
        self.X = np.matrix(self.X)
        self.X_transpose = np.matrix(self.X).getT()
        
        # (X'X)^-1
        X_transp_X = np.matmul(self.X_transpose, self.X)
        self.X_transp_X_inv = X_transp_X.getI()
        # X'y
        self.X_transp_y = np.matmul(self.X_transpose, self.y)

    def estimate_betas_and_yhat(self):
        # betas = (X'X)^-1 * X'y
        self.betas = np.matmul(self.X_transp_X_inv, self.X_transp_y)
        # y-hat = X * betas
        self.y_hat = np.matmul(self.X, self.betas)
        # Create a column that holds y_hat values
        self.data[self.y_name + " estimator"] = [i.item(0) for i in self.y_hat]
        # create a table that holds the estimated coefficient
        # this will also be used to store SEs, t-stats, and p-values
        self.estimates = pd.DataFrame(self.betas, index = self.beta_names,
                                           columns = ["Coefficient"])
        # identify y variable in index
        self.estimates.index.name = "y = " + self.y_name
        
    def calculate_regression_stats(self):
        self.sum_square_stats()
        self.calculate_degrees_of_freedom()
        self.calculate_estimator_variance()
        self.calculate_covariance_matrix()  
        self.calculate_t_p_error_stats()
        self.calculate_MSE()
        self.calculate_rsquared()
        self.calculate_fstat()
        
    def sum_square_stats(self):
        ssr_list = []
        sse_list = []
        sst_list = []
        mean_y = self.stats.mean(self.y).item(0)
        for i in range(len(self.y)):
            # ssr is sum of squared distances between the estimated y values
            # (y-hat) and the average y-value (y-bar)
            yhat_i = self.y_hat[i]
            y_i = self.y[i]
            ssr_list.append((yhat_i - mean_y) ** 2)
            sse_list.append((y_i - yhat_i) ** 2)
            sst_list.append((y_i - mean_y) ** 2)
        # call item - to for value instead of matrix
        self.ssr = self.stats.total(ssr_list).item(0)
        self.sst = self.stats.total(sst_list).item(0)
        self.sse = self.stats.total(sse_list).item(0)

    def calculate_degrees_of_freedom(self):
        # Degrees of freedom compares the number of observations to the number
        # of variables used to form prediction
        self.lost_degrees_of_freedom = len(self.estimates)
        self.degrees_of_freedom = (self.max_val + 1 - self.min_val ) \
                            - self.lost_degrees_of_freedom 

    def calculate_estimator_variance(self):
        # estimator variance is the sse normalized by the degrees of freedom
        # thus, there is a tradeoff between estimator variance and degrees of
        # of freedom
        self.estimator_variance = self.sse / self.degrees_of_freedom

    def calculate_covariance_matrix(self):
        # Covariance matrix will be used to estimate standard errors for
        # each coefficient
        # est_var * (X'X)^-1 is the covariance matrix
        self.cov_matrix = copy.copy(self.X_transp_X_inv)
        if self.estimator_variance != None:
            self.cov_matrix = float(self.estimator_variance) * self.cov_matrix
        self.cov_matrix = pd.DataFrame(self.cov_matrix, 
                                       columns = self.beta_names,
                                       index = self.beta_names)
        
    def calculate_t_p_error_stats(self):
        est = ["SE", "t-stat", "p-value", "p-rating"]
        rating_dict = {.001:"***",
                       .01:"**",
                       .05:"*"}
        for name in est: 
            results = self.estimates
            results[name] = np.nan
            for var in self.beta_names:
                if name == "SE": 
                    # SE of coefficient is found in the diagonal of cov_matrix
                    results.ix[var][name] = \
                    self.cov_matrix[var][var] ** (1/2)
                if name == "t-stat":
                    # tstat = Coef / SE
                    results.ix[var][name] = \
                    results.ix[var]["Coefficient"] / results.ix[var]["SE"]
                if name == "p-value":
                    # p-values is estimated from location within a 
                    # distribution implied by the t-stat
                    results.ix[var][name] = round(t.sf(\
                              np.abs(results.ix[var]["t-stat"]), 
                              self.degrees_of_freedom + 1) * 2, 5)
                if name == "p-rating":
                    print(name)
                    for val in rating_dict:
                        if results.ix[var]["p-value"] < val:
                            results[name][var] = rating_dict[val]
                            break
                        # if p-stat > .05, no break in for-loop, set val of ""
                        results[name][var] = ""
                
    
    def calculate_MSE(self):
        self.mse = self.estimator_variance ** (1/2)
    
    def calculate_rsquared(self):
        self.r_sq = self.ssr / self.sst
    
    def calculate_fstat(self):
        self.f_stat = ((self.sst - self.sse) / (self.lost_degrees_of_freedom \
                       - 1)) / (self.estimator_variance)

    def build_stats_DF(self):
        stats_dict = {"r**2":[self.r_sq],
                     "f-stat":[self.f_stat], 
                     "Est Var": [self.estimator_variance],
                     "MSE":[self.mse],
                     "SSE":[self.sse],
                     "SSR":[self.ssr], 
                     "SST":[self.sst]}
        self.stats_DF = pd.DataFrame(stats_dict)
        self.stats_DF = self.stats_DF.rename(index={0:"Estimation Statistics"})
        self.stats_DF = self.stats_DF.T