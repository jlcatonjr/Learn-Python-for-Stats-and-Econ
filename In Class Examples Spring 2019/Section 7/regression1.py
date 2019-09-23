from stats import *
import pandas as pd
import numpy as np
import copy 
from scipy.stats import t

class Regression():
    def __init__(self):
        self.stats = Stats()
    def regress(self, reg_name, data, y_name, beta_names, min_val = 0,
                max_val = None, constant = True):
        self.min_val = 0
        if max_val != None:
            self.max_val = max_val
        else:
            self.max_val = len(data)
        self.reg_name = reg_name
        self.data = copy.copy(data)
        self.y_name = y_name
        self.beta_names = copy.copy(beta_names)
        if constant:
            self.add_constant()
        self.build_matrices()
        self.calculate_regression_stats()
        self.build_summary()
        
    def add_constant(self):
        self.data["Constant"] = 1
        self.beta_names.append("Constant")

    def build_matrices(self):
        # Transform dataframes to matrices
        self.y = np.matrix(self.data[self.y_name]\
                                        [self.min_val:self.max_val]).getT()
        # create standard array of X values
        self.X = self.data[self.beta_names].values
        # create standard array of X values
        self.X = np.matrix(self.X)
        self.X_transpose = np.matrix(self.X).getT()
        
        #(X'X)^-1
        X_transp_X = np.matmul(self.X_transpose, self.X)
        X_transp_X_Inv = X_transp_X.getI()
        
        #X'Y
        X_transp_y = np.matmul(self.X_transpose, self.y)
        self.Betas = np.matmul(X_transp_X_Inv, X_transp_y)
        
        # y-hat = X * Betas
        self.y_hat = np.matmul(self.X, self.Betas)
        self.data[self.y_name + " estimator"] = [i.item(0) for i in self.y_hat]
        
        self.beta_estimates = pd.DataFrame(self.Betas, index = self.beta_names,
                                        columns = ["Coefficient"])

    def calculate_regression_stats(self):
        self.sum_square_stats()
        self.calculate_estimator_variance()
        self.calculate_rsquared()
        self.calculate_fstat()
        self.build_stats_DF()
        self.regression_covariance_matrix()
        self.calculate_t_p_error_stats()
        
    def sum_square_stats(self):
        self.ssr_list = []
        self.sse_list = []
        self.sst_list = []
        mean_y = self.stats.mean(self.y).item(0)
        for i in range(len(self.y)):
            # ssr is sum of squared distances between the estimated y values,
            # y-hat, and the average y-value
            yhat_i = self.y_hat[i]
            y_i = self.y[i]
            self.ssr_list.append((yhat_i - mean_y) ** 2)
            self.sse_list.append((y_i - yhat_i) ** 2)
            self.sst_list.append((y_i - mean_y) ** 2)
        # call item 0 to for value instead of matrix
        self.ssr = self.stats.total(self.ssr_list).item(0)
        self.sst = self.stats.total(self.sst_list).item(0)
        self.sse = self.stats.total(self.sse_list).item(0)
    
    def calculate_estimator_variance(self):
        self.lost_degrees_of_freedom = len(self.beta_estimates)
        self.degrees_of_freedom = (self.max_val + 1 - self.min_val ) \
                            - self.lost_degrees_of_freedom 
        self.estimator_variance = self.sse / self.degrees_of_freedom
        self.mse = self.estimator_variance ** (1/2)
    def calculate_rsquared(self):
        self.r_sq = self.ssr / self.sst
    
    def calculate_fstat(self):
        self.f_stat = ((self.sst - self.sse) / (self.lost_degrees_of_freedom \
                       - 1)) / (self.estimator_variance)
    

        
    def regression_covariance_matrix(self):
        self.cov_matrix = np.matmul(self.X_transpose, self.X).getI()
        if self.estimator_variance != None:
            self.cov_matrix = float(self.estimator_variance) * self.cov_matrix
        self.cov_matrix = pd.DataFrame(self.cov_matrix, columns = self.beta_names,
                                       index = self.beta_names)
        
    def calculate_t_p_error_stats(self):
        est = ["SE", "t-stat", "p-value"]
        for name in est: 
            results = self.beta_estimates
            results[name] = np.nan
            for var in self.beta_names:
                if name == "SE": 
                   results.ix[var][name] = \
                    self.cov_matrix[var][var] ** (1/2)
                if name == "t-stat":
                    results.ix[var][name] = \
                    results.ix[var]["Coefficient"] / results.ix[var]["SE"]
                if name == "p-value":
                    results.ix[var][name] = round(t.sf(np.abs(results.ix[var]["t-stat"]), 
                              self.degrees_of_freedom + 1) * 2, 5)
        results.index.name = "y = " + self.y_name
    def build_stats_DF(self):
        stats_dict = {"r**2":[self.r_sq],
                     "f-stat":[self.f_stat], 
                     "Est Var": [self.estimator_variance],
                     "SSE":[self.sse],
                     "SSR":[self.ssr], 
                     "SST":[self.sst]}
        self.stats_DF = pd.DataFrame(stats_dict)
        self.stats_DF.name = "Estimation Statistics"

    def build_summary(self):
        self.summary = {self.beta_estimates.index.name:self.beta_estimates}
        self.summary[self.stats_DF.name] =  self.stats_DF.T