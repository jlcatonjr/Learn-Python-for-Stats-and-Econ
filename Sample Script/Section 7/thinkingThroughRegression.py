import pandas as pd
import numpy as np

def regression(data, y_name, X_names, constant = True):
    if constant: add_constant(data, X_names)
    # Transform dataframes to matrices
    y = np.matrix(data[y_name]).getT()
    # create a k x n nested list containing vectors for each xi
    X = data[X_names].values
    # create X Array
    X = np.matrix(X)

    X_transpose = np.matrix(X.getT())
    # (X'X)^-1
    X_transp_X = np.matmul(X_transpose, X)
    X_transp_X_inv = X_transp_X.getI()
    print("X:\n", X)
    print("y:\n", y)
    print("X_transpose:", X_transpose)
    print("X_transp_X:\n", X_transp_X)
    print("X_transp_X_inv:\n", X_transp_X_inv)
    #X'y
    X_transp_y = np.matmul(X_transpose, y)
    print("X_transp_y:\n", X_transp_y)
    print("betas = (X'X)^-1 * X'y")
#    # betas = (X'X)^-1 * X'y
    betas = np.matmul(X_transp_X_inv, X_transp_y)
    print("betas:\n", betas)
    # y-hat = X * betas
    y_hat = np.matmul(X, betas)
    print("y_hat:", y_hat)
    # Create a column that holds y_hat values
    print()
    for i in y_hat: print(i.item(0))
    data[y_name + " estimator"] = [i.item(0) for i in y_hat]
    # create a table that holds the estimated coefficient
    # this will aslo be used to store SEs, t-stats, and p-values
    estimates = pd.DataFrame(betas, index = X_names,
                     columns = ["Coefficient"])
    # identify y variable in index
    estimates.index.name ="y = " + y_name
#    print(estimates)
#    
def add_constant(data, X_names):
    data["Constant"] = 1
    if "Constant" not in X_names:
        X_names.append("Constant")

  

data = pd.read_csv("cleanedEconFreedomData.csv", index_col=[0])

y_name = "5 Year GDP Growth Rate (%)"
X_names = ["GDP per Capita (PPP)"]
regression(data, y_name, X_names)