#fixedEffectsRegression.py
import pandas as pd
import regression
data = pd.read_csv("fraserDataWithRGDPPC.csv", index_col=[0,1], 
                             parse_dates = True)
data["RGDP Per Capita Lag"] = data.groupby(level=0)["RGDP Per Capita"].shift(-1)
data = data.dropna()
restrict_name ="Restricted Econ Freedom Panel Reg"
unrestrict_name = "Unrestricted Econ Freedom Panel Reg"
X_names = ["RGDP Per Capita Lag"]
y_name = ["RGDP Per Capita"]

# create new column of data to mark countries that are in North America
reg = regression.Regression()
reg.panel_regression(reg_name = restrict_name, data = data,
        y_name = y_name, beta_names = X_names, entity=True)
X_names = ["SUMMARY INDEX", "RGDP Per Capita Lag"]
y_name = ["RGDP Per Capita"]
reg.panel_regression(reg_name = "Unrestricted Econ Freedom Panel Reg", data = data,
        y_name = y_name, beta_names = X_names, entity=True)
f_stat = reg.joint_f_test(restrict_name, unrestrict_name)
print(f_stat)