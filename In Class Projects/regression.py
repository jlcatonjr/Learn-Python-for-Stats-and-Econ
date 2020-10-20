#regression.py
import pandas as pd
import copy
from stats import *
import numpy as np

class Regression:
    def __init__(self):
        self.stats = stats()
    
    # if constant is True, add a column of ones to 
    # estimate a constant
    def OLS(self, reg_name, data, y_name, beta_names,
            min_val = 0, max_val = None,
            constant = True):
    
        self.min_val = min_val
        if max_val != None:
            self.max_val = max_val
        else:
            self.max_val = len(data)
        self.reg_name = reg_name
        self.y_name = y_name
        
        self.beta_names = copy.copy(beta_names)
        self.data = data.copy()
        if constant:
            self.add_constant()
        self.build_matrices()
        self.estimate_betas_and_yhat()
        self.calculate_regression_stats()
        
    def calculate_regression_stats(self):
        self.sum_square_stats()
    
    def sum_square_stats(self):
        ssr_list = []
        sse_list = []
        sst_list = []
        mean_y = self.stats.mean(self.y).item(0)
        for i in range(len(self.y)):
            # ssr is sum of squared distances between the estimates
            # and the avergage of y values
            y_hat_i = self.y_hat[i]
            y_i = self.y[i]
            r = y_hat_i - mean_y
            e = y_i - y_hat_i
            t = y_i - mean_y
            ssr_list.append((r) ** 2)
            sse_list.append((e) ** 2)
            sst_list.append((t) ** 2)
            
        self.ssr = self.stats.total(ssr_list).item(0)
        self.sse = self.stats.total(sse_list).item(0)
        self.sst = self.stats.total(sst_list).item(0)
    
    def add_constant(self):
        self.data["Constant"] = 1
        self.beta_names.append("Constant")
            
    def build_matrices(self):
        # Transform dataframes to matrices
        self.y = np.matrix(self.data[self.y_name][self.min_val:self.max_val])
        # create a k X n nested lest containing vectors from each exog var
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
        # y-hat = X * betas
        self.y_hat = np.matmul(self.X, self.betas)
        self.data[self.y_name[0] + " estimator"] =\
            [i.item(0) for i in self.y_hat]
        # create a table for the estimates
        self.estimates = pd.DataFrame(self.betas, index = self.beta_names,
                                      columns = ["Coefficient"])
        # identify y vairiable in index
        self.estimates.index.name = "y = " + self.y_name[0]
            























