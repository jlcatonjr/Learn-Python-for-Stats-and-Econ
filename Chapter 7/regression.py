#regression.py
import pandas as pd
from stats import *
import numpy as np
from scipy.stats import t, f

class Regression:
    def __init__(self):
        self.stats = Stats()
        self.reg_history = {}
        
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
        self.calculate_regression_stats()
        self.save_output()
        
    def add_constant(self):
        self.data["Constant"] = 1
        self.beta_names.append("Constant")
        
    def build_matrices(self):
        # Transform dataframes to matrices
        self.y = np.matrix(self.data[self.y_name][self.min_val:self.max_val])
        # create a k X n nested list containg vectors for each exogenous var
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
        # Create a column that holds y-hat values
        self.data[self.y_name[0] + " estimator"] = \
            [i.item(0) for i in self.y_hat]
        # create a table that holds the estimated coefficient
        # this will also be used to store SEs, t-stats,and p-values
        self.estimates = pd.DataFrame(self.betas, index = self.beta_names,
                                      columns = ["Coefficient"])
        # identify y variable in index
        self.estimates.index.name = "y = " + self.y_name[0]
        
    def calculate_regression_stats(self):
        self.sum_square_stats()
        self.calculate_degrees_of_freedom()
        self.calculate_estimator_variance()
        self.calculate_covariance_matrix()
        self.calculate_t_p_error_stats()
        self.calculate_MSE()
        self.calculate_rsquared()
        self.calculate_fstat()
        self.build_stats_DF()
    
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
            ssr_list.append((yhat_i - mean_y) ** 2)
            sse_list.append((y_i - yhat_i) ** 2)
            sst_list.append((y_i - mean_y) ** 2)
            # call item - call value instead of matrix
            self.ssr = self.stats.total(ssr_list).item(0)
            self.sst = self.stats.total(sst_list).item(0)
            self.sse = self.stats.total(sse_list).item(0)

    def calculate_degrees_of_freedom(self):
        # Degrees of freedom compares the numer of observations to the number 
        # of exogenous variables used to form the prediction
        self.lost_degrees_of_freedom = len(self.estimates)
        self.num_obs = self.max_val + 1 - self.min_val
        self.degrees_of_freedom =  self.num_obs - self.lost_degrees_of_freedom
        
    def calculate_estimator_variance(self):
        # estimator variance is the sse normalized by the degrees of freedom
        # thus, estimator variance increases as the number of exogenous 
        # variables used in estimation increases (i.e., as degrees of freedom
        # fall)
        self.estimator_variance = self.sse / self.degrees_of_freedom
        
    def calculate_covariance_matrix(self):
        # Covariance matrix will be used to estimate standard errors for
        # each coefficient.
        # estimator variance * (X'X)**-1 is the covariance matrix
        self.cov_matrix = float(self.estimator_variance) * self.X_transp_X_inv
        self.cov_matrix = pd.DataFrame(self.cov_matrix, 
                                       columns = self.beta_names,
                                       index = self.beta_names)
    
    def calculate_t_p_error_stats(self):
        self.rating_dict = {.05:"*",
                       .01:"**",
                       .001: "***"}
        results = self.estimates
        stat_sig_names = ["SE", "t-stat", "p-value"]
        for stat_name in stat_sig_names: 
            results[stat_name] = np.nan
        # generate statistic for each variable
        for var in self.beta_names:
            # SE of coefficient is found in the diagonal of cov_matrix
            results.loc[var]["SE"] = self.cov_matrix[var][var] ** (1/2)
            # tstat = Coef / SE
            results.loc[var]["t-stat"] = \
                results["Coefficient"][var] / results["SE"][var]
            # p-value is estimated using a  table that transforms t-value in 
            # light of degrees of freedom
            results.loc[var]["p-value"] = np.round(t.sf(np.abs(results.\
                       loc[var]["t-stat"]),self.degrees_of_freedom + 1) * 2, 5)
        # values for signifiances will be blank unless p-value < .05
        # pandas does not allow np.nan values or default blank strings to 
        # be replaced ex post...
        significance = ["" for i in range(len(self.beta_names))]   
        for i in range(len(self.beta_names)):
            var = self.beta_names[i]
            for val in self.rating_dict:
                if results.loc[var]["p-value"] < val:
                    significance[i] = self.rating_dict[val]
                    print(var, self.rating_dict[val])  
        results["significance"] = significance
        
    def calculate_MSE(self):
        self.mse = self.estimator_variance ** (1/2)
    
    def calculate_rsquared(self):
        self.r_sq = self.ssr / self.sst
        self.adj_r_sq = 1 - self.sse / self.degrees_of_freedom / (self.sst\
                             / (self.num_obs - 1))
    
    def calculate_fstat(self):
        self.f_stat = (self.sst - self.sse) / (self.lost_degrees_of_freedom\
                       - 1) / self.estimator_variance
    
    def build_stats_DF(self):
        stats_dict = {"r**2": [self.r_sq],
                      "Adj. r**2": [self.adj_r_sq],
                      "f-stat": [self.f_stat],
                      "EST Var": [self.estimator_variance],
                      "MSE": [self.mse],
                      "SSE": [self.sse],
                      "SSR": [self.ssr],
                      "SST": [self.sst],
                      "Obs.": [self.num_obs],
                      "DOF":[self.degrees_of_freedom]}
        self.stats_DF = pd.DataFrame(stats_dict)
        self.stats_DF = self.stats_DF.rename(index={0:"Estimation Statistics"})
        self.stats_DF = self.stats_DF.T

    def save_output(self):
        self.reg_history[self.reg_name] = {}
        self.reg_history[self.reg_name]["Reg Stats"] = self.stats_DF.copy()
        self.reg_history[self.reg_name]["Estimates"]= self.estimates.copy()
        self.reg_history[self.reg_name]["Cov Matrix"] = self.cov_matrix.copy()
        
    def joint_f_test(self, reg1_name, reg2_name):
        # identify data for each regression
        reg1 = self.reg_history[reg1_name]
        reg2 = self.reg_history[reg2_name]
        # identify beta estimates for each regression to draw variables
        reg1_estimates = reg1["Estimates"]        
        reg2_estimates = reg2["Estimates"]
        # name of y_var is saved as estimates index name
        reg1_y_name = reg1_estimates.index.name
        reg2_y_name = reg2_estimates.index.name
        num_obs1 = reg1["Reg Stats"].loc["Obs."][0]
        num_obs2 = reg2["Reg Stats"].loc["Obs."][0]
        # check that the f-stat is measuring restriction,not for diff data sets  
        if num_obs1 != num_obs2: 
            self.joint_f_error()
        if reg1_y_name == reg2_y_name:        
            restr_reg = reg1 if \
                len(reg1_estimates.index) < len(reg2_estimates.index) else reg2
            unrestr_reg = reg2 if restr_reg is reg1 else reg1
            restr_var_names = restr_reg["Estimates"].index
            unrestr_var_names = unrestr_reg["Estimates"].index
        # identify statistics for each regression
        restr_reg = restr_reg if False not in \
                [key in unrestr_var_names for key in restr_var_names] else None
        if restr_reg == None:
            self.joint_f_error()
        else:
            sser = restr_reg["Reg Stats"].loc["SSE"][0]
            sseu = unrestr_reg["Reg Stats"].loc["SSE"][0]
            dofr = restr_reg["Reg Stats"].loc["DOF"][0]     
            dofu = unrestr_reg["Reg Stats"].loc["DOF"][0]
            dfn = dofr - dofu
            dfd = dofu - 1
            f_stat = ((sser - sseu) / (dfn)) / (sseu / (dfd))
            f_crit_val = 1 - f.cdf(f_stat,dfn = dfn, dfd = dfd)
            #make dictionary?
            f_test_label = ""
            for key in unrestr_var_names:
                if key not in restr_var_names:
                    f_test_label = f_test_label + str(key) + " = "
            f_test_label = f_test_label + "0"
            res_dict = {"f-stat":[f_stat],
                        "p-value":[f_crit_val],
                        "dfn":[dfn],
                        "dfd":[dfd]}
            res_DF = pd.DataFrame(res_dict)
            res_DF = res_DF.rename(index={0:""})
            res_DF = res_DF.T
            res_DF.index.name = f_test_label
            
            return res_DF
            
    def joint_f_error(self):
            print("Regressions not comparable for joint F-test")
            return None
            