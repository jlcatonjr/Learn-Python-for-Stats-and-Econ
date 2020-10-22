#regression.py
import pandas as pd
import copy
from stats import *
import numpy as np
from scipy.stats import t, f

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
        
    def add_constant(self):
        self.data["Constant"] = 1
        self.beta_names.append("Constant")
        
    def estimate_betas_and_yhat(self):
        # betas = (X'X)**-1 * X'y
        self.betas = np.matmul(self.X_transp_X_inverse, self.X_transp_y)
        # y-hat = X * betas
        self.y_hat = np.matmul(self.X, self.betas)
        self.data[self.y_name[0] + " estimator"] =\
            [i.item(0) for i in self.y_hat]
        # create a table for the estimates
        self.estimates = pd.DataFrame(self.betas, index = self.beta_names,
                                      columns = ["Coefficient"])
        # identify y vairiable in index
        self.estimates.index.name = "y = " + self.y_name[0]
            
            
    def build_matrices(self):
        # Transform dataframes to matrices
        self.y = np.matrix(self.data[self.y_name][self.min_val:self.max_val])
        # create a k X n nested lest containing vectors from each exog var
        self.X = np.matrix(self.data[self.beta_names])
        self.X_transpose = np.matrix(self.X).getT()
        # (X'X)**-1
        X_transp_X = np.matmul(self.X_transpose, self.X)
        self.X_transp_X_inverse = X_transp_X.getI()
        # X'y
        self.X_transp_y = np.matmul(self.X_transpose, self.y)
        

    def calculate_regression_stats(self):
        self.sum_square_stats()
        self.calculate_degrees_of_freedom()
        self.calculate_estimator_variance()
        self.calculate_covariance_matrix()
        self.calculate_t_p_error_stats()
        self.calculate_root_MSE()
        self.calculate_rsquared()
        self.calculate_fstat()
        self.build_stats_DF()
        
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
        
        # since the ssr, sse, and sst use values from 
        # matrices, select the value within the resultant
        # matrix using matrix.item(0)
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
        # estimator variance is the sse normalized by the degrees of freedom  
        # thus, estimator variance increases as the number of exogenous  
        # variables used in estimation increases(i.e., as degrees of freedom   
        # fall) 
        self.estimator_variance = self.sse / self.degrees_of_freedom
    
    def calculate_covariance_matrix(self):
        # Covariance matrix will be used to estimate standard errors for  
        # each coefficient.  
        # estimator variance * (X'X)**-1  
        self.cov_matrix = float(self.estimator_variance) * self.X_transp_X_inverse
        self.cov_matrix = pd.DataFrame(self.cov_matrix,
                                  columns = self.beta_names,
                                  index = self.beta_names)
        
    def calculate_t_p_error_stats(self):
        results = self.estimates
        stat_sig_names = ["SE", "t-stat", "p-value"]
        # create space in data frame for SE, t, and p
        for stat_name in stat_sig_names:
            results[stat_name] = np.nan
        # generate statistic for each variable
        for var in self.beta_names:
            # SE ** 2 of coefficient is found in the diagonal of the cov_matrix
            results.loc[var]["SE"] = self.cov_matrix[var][var] ** (1/2)     
            # t-stat = Coef / SE
            results.loc[var]["t-stat"] = \
                results["Coefficient"][var] / results["SE"][var]
            # p-values is estimated using a table that transforms t-stat in   
            # light of degrees of freedom  
            # 2 is for 2 tail...
            # 5 is to round to 5 decimal places
            results.loc[var]["p-value"] = np.round(
                t.sf(np.abs(results.loc[var]["t-stat"]), 
                     self.degrees_of_freedom +1) * 2, 5)
        ratings = [.05, .01, .001]
        significance = ["" for name in self.beta_names]
        for i in range(len(self.beta_names)):
            var = self.beta_names[i]
            for rating in ratings:
                if results.loc[var]["p-value"] < rating:
                    significance[i] = significance[i] + "*"
        results["significance"] = significance

    def calculate_root_MSE(self):
        self.root_mse = self.estimator_variance ** (1/2)
    
    def calculate_rsquared(self):
        self.r_sq = self.ssr / self.sst
    
    def calculate_fstat(self):
        self.f_stat = (self.sst - self.sse) / (self.lost_degrees_of_freedom\
                                               - 1) / self.estimator_variance
    
    def build_stats_DF(self):
        stats_dict = {"r**2": [self.r_sq],
                      "f-stat":[self.f_stat],
                      "Est Var":[self.estimator_variance],
                      "rootMSE":[self.root_mse],
                      "SSE":[self.sse],
                      "SSR": [self.ssr],
                      "SST":[self.sst],
                      "Obs.":[int(self.num_obs)],
                      "DOF":[int(self.degrees_of_freedom)]}
        self.stats_DF = pd.DataFrame(stats_dict)
        self.stats_DF = self.stats_DF.rename(index = {0:"Estimation Statistics"})
        self.stats_DF = self.stats_DF.T 
















