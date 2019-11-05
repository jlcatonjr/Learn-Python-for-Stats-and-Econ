#regression.py
import pandas 
import numpy as np
from stats import *

class Regression:
    def __init__(self):
        self.stats = Stats()
    
    def OLS(self, reg_name, data, y_name, beta_names, min_val = 0,
            max_val = None, constant = True):
        self.min_val = min_val
        if max_val != None:
            self.max_val = max_val
        else:
            self.max_val = len(data)
        self.reg_name = reg_name
        self.y_name = y_name
        self.beta_names = beta_names
        self.data = data.copy()
        if constant:
            self.add_constant()
        self.build_matrices()
        self.estimate_betas_and_yhat()
    
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
        print(self.y_hat)
        
        
        
        
        