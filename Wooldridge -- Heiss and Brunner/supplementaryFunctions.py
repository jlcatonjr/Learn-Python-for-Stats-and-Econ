import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
def OLS_summary(results, round_dig = 4):
    summary = {"$\\beta $":results.params, 
               "$t$": results.tvalues,
               "$$P>|t|$$":results.pvalues,
               # calculate standard errors by taking the square root of the variance values 
               # along the diagonal of the covariance matrix 
              "$SE$":[results.cov_params()[var][var] ** (.5) for var in results.cov_params()]}
    summary = pd.DataFrame(summary)
    # add r^2 using index name
    summary.index.name = "$$r^2: "+str(round(results.rsquared,round_dig)) + "$$"
    
    return summary.round(round_dig)

def LM_summary(results, round_dig = 4):
    summary = {"$\\beta $":results.params, 
           "$t$": results.tstats,
           "$$P>|t|$$":results.pvalues,
           # calculate standard errors by taking the square root of the variance values 
           # along the diagonal of the covariance matrix 
          "$SE$":results.std_errors}
    summary = pd.DataFrame(summary)
    # add r^2 using index name
    summary.index.name = "$$r^2: "+str(round(results.rsquared,round_dig)) + "$$"
    
    return summary.round(round_dig)

def build_estimator(data, results, y_name):
    data["$$\widehat{" + y_name + "}$$"] = results.fittedvalues
    data["$$\hat{u}$$"] = results.resid
    

def plot_errors(data):
    plot_data = data.rename(columns = {key:key.replace("$$","$") for key in data.keys()})
    names = list(plot_data.keys())[:-2]
    y_name, x_names = names[0],names[1:]
# matplotlib rejects keys with $$, replace with $
    for x_name in x_names:    
        fig, ax = plt.subplots(figsize = (20,10))
        plot_data.plot.scatter(x = x_name, 
                                y = "$\hat{u}$", 
                                ax = ax)
        # Check SLR4
        error_corr = plot_data.corr().round(2)["$\hat{u}$"][x_name]
        plt.title("Correlation: " + str(error_corr))
        
        
def build_X_y_matrices(data, names, log_vars = None, constant = True):
    if type(log_vars) is list:
        for name in log_vars:
            data[name] = np.log(data[name])
    y_name, x_names = names[0], names[1:]
    X = data[x_names]
    if constant:
        X["Intercept"] = 1
    y = data[[y_name]]
    
    return X, y

def regression_df(reg):
    reg_df= reg.data.orig_endog
    reg_df[list(reg.data.orig_exog.keys())]  = reg.data.orig_exog
    
    return reg_df

def build_smooth_multiple_regression_estimator(reg, orig_df):
    def find_between_from_list(lst, start, end):
        for i in range(len(lst)):
            s = lst[i]
            if start in s and end in s:
                lst[i] = (s.split(start))[1].split(end)[0]
        return lst    
    results = reg.fit()
    df = reg.data.frame
    orig_names =  find_between_from_list(list(reg.data.orig_endog.keys()) + list(reg.data.orig_exog.keys()), "(", ")")
    y_var, X_vars = orig_names[0], orig_names[1:]
    X_vars = [x for x in X_vars if x != "Intercept" and x in df.keys()]
    for x_name in X_vars:
        x_min, x_max = df[x_name].describe()[["min","max"]]
        X = pd.DataFrame({x_name: np.linspace(x_min, x_max, num = 1000)})
        keys = [x for x in X_vars if x != x_name]
        X[keys] = df[keys].mean()
        lpr_PICI = results.get_prediction(X).summary_frame(alpha = 0.05)
        lpr_PICI.index = X[x_name]
        lpr_CI = lpr_PICI[["mean", "mean_ci_lower", "mean_ci_upper"]]
        fig, ax = plt.subplots(figsize = (20,10))
        for key in lpr_CI:
            ls, alpha = ("--", .5) if "ci" in key else ("-", 1)
            lpr_CI[[key]].plot(ls = ls, 
                               linewidth = 3, 
                               alpha = alpha, color = "C0", ax = ax)
        ax.set_xlabel(x_name)
        ax.set_ylabel(y_var)
        scatter_df = df.copy()
        orig_yname =  list(reg.data.orig_endog.keys())[0]
        orig_y = reg.data.orig_endog[orig_yname]
        print(orig_yname)
        scatter_df[y_var] = orig_y
        scatter_df.groupby(x_name).mean()[y_var].reset_index().plot.scatter(x = x_name, y = y_var, 
                                                                                ax = ax, color = "k", alpha = .75)
    