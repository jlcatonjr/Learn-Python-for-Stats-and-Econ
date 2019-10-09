#indicatorVariable.py
import pandas as pd
import regression

def create_indicator_variable(data, indicator_name, index_name, target_index_list):
    # Prepare column with name of indicator variable
    data[indicator_name] = 0
    # for each index whose name matches an entry in target_index_list
    # a value of 1 will be recorded
    for index in target_index_list:
        data[indicator_name].loc[(data.index.get_level_values(\
            index_name)== index)] = 1



# Import data with "ISO_Code" and "Year" as index columns
data = pd.DataFrame.from_csv("fraserDataWithRGDPPC.csv", index_col=[0,1], 
                             parse_dates = True)

index_name = "ISO_Code"
indicator_name = "North America"
# Cuba, Grenada, Saint Kitts, Saint Lucia, Saint Vincent are missing 
# from Fraser data
countries_in_north_america = ["BHS", "BRB", "BLZ", "CAN", "CRI", "DOM",
                              "SLV", "GTM", "HTI", "HND", "JAM", "MEX",
                              "NIC", "PAN", "PAN", "TTO", "USA"]
# create new column of data to mark countries that are in North America
create_indicator_variable(data = data, indicator_name = indicator_name, 
      index_name = index_name, target_index_list = countries_in_north_america)
data["Real GDP Lag"] = data.groupby(level=0)["RGDP Per Capita"].shift(-1)

# prepare regression variables
reg_name = "Regression with Indicator Variable"
X_names = ["SUMMARY INDEX", "Real GDP Lag", "North America"]
y_name = ["RGDP Per Capita"]
#save instance of regression class
reg = regression.Regression()
# call regression method
reg.regress(reg_name = reg_name, data = data.dropna(), 
            y_name = y_name, X_names = X_names)