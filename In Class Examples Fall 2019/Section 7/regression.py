#regression.py
import pandas as pd
import numpy as np
import copy
from stats import *

class Regression:
    def __init__(self):
        self.stats = Stats()
    
    def OLS(self, reg_name, data, y_name, beta_names, min_val = 0,
            max_val = None, constant = True):
        # min_val and max_val set index range by index number
        self.min_val = min_val
        if max_val != None:
            self.max_val = max_val
        else:
            self.max_val = len(data)
        self.reg_name = reg_name
        # enodogenous variable name
        self.y_name = y_name
        # names of X variables
        self.beta_names = copy.copy(beta_names)
        #make a copy of the data that is passed to OLS
        self.data = data.copy()
        # if the OLS regression has a constant, add column of 1s to data
        if constant:
            self.add_constant()
        self.build_matrices() 
        self.estimate_betas_and_yhat()
        self.calculate_regression_stats()
    
    def add_constant(self):
        self.data["Constant"] = 1
        self.beta_names.append("Constant")
    
    def build_matrices(self):
        # Transform dataframews to matrices
        self.y = np.matrix(self.data[self.y_name][self.min_val:self.max_val])
        # create a k X n nested list containing vectors for each exogenous var
        self.X = np.matrix(self.data[self.beta_names])
        self.X_transpose = np.matrix(self.X).getT()
        # (X'X)**-1
        X_transp_X = np.matmul(self.X_transpose, self.X)
        self.X_transp_X_inv = X_transp_X.getI()
        # X'y
        self.X_transp_y = np.matmul(self.X_transpose, self.y)
        
    def estimate_betas_and_yhat(self):
        # betas = (X'X)**-1 * X'y
        self.betas = np.matmul(self.X_transp_X_inv, self.X_transp_y)
        # y_hat = X * betas
        self.y_hat = np.matmul(self.X, self.betas)
        # Create a column that hold y-hat values
        #.item(n) pulls nth value from matrix
        self.data[self.y_name[0] + " estimator"] = \
            [i.item(0) for i in self.y_hat]
        # create a table that holds the estimated coefficient
        # this will also be used to store SEs, t-stats, and p-values
        self.estimates = pd.DataFrame(self.betas, index = self.beta_names,
                                      columns = ["Coefficient"])
        # identify y variable in index
        self.estimates.index.name = "y = " + self.y_name[0]        
        
    def calculate_regression_stats(self):
        self.sum_square_stats()
        self.calculate_degrees_of_freedom()
        self.calculate_estimator_variance()
        self.calculate_covariance_matrix()
    def sum_square_stats(self):
        ssr_list = []
        sse_list = []
        sst_list = []
        mean_y = self.stats.mean(self.y).item(0)
        for i in range(len(self.y)):
            # ssr is sum of squared distances between the estimated y values
            # (y-hat) and the average of y values (y-bar)
            yhat_i = self.y_hat[i]
            y_i = self.y[i]
            r = yhat_i - mean_y
            e = y_i - yhat_i
            t = y_i - mean_y
            ssr_list.append((r) ** 2)
            sse_list.append((e) ** 2)
            sst_list.append((t) ** 2)
        # call item - call value instead of matrix
        self.ssr = self.stats.total(ssr_list).item(0)
        self.sse = self.stats.total(sse_list).item(0)
        self.sst = self.stats.total(sst_list).item(0)
        
    def calculate_degrees_of_freedom(self):
        # Degrees of freedom compares the number of observations to the number
        # of exogenous variables used to form the prediction
        self.lost_degrees_of_freedom = len(self.estimates)
        self.num_obs = self.max_val + 1 - self.min_val
        self.degrees_of_freedom = self.num_obs - self.lost_degrees_of_freedom
        
    def calculate_estimator_variance(self):
#        estimator variance is the sse normalized by the degrees of freedom
        # thus, estimator variance increases as the number of exogenous
        # variables used in estimation increases(i.e., as degrees of freedom 
        # fall)
        self.estimator_variance = self.sse / self.degrees_of_freedom
        
    def calculate_covariance_matrix(self):
        # Covariance matrix will be used to estimate standard errors for
        # each coefficient.
        # estimator variance * (X'X)**-1
        self.cov_matrix = float(self.estimator_variance) * self.X_transp_X_inv
        self.cov_matrix = pd.DataFrame(self.cov_matrix,
                                       columns = self.beta_names,
                                       index = self.beta_names)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    