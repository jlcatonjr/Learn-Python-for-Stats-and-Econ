#indicatorVariable.py
import pandas as pd

def create_indicator_variable(data, indicator_name, index_name, 
                              target_index_list):
    # Prepare column with name of indicator variable
    data[indicator_name] = 0
    # for each index whose name matches an entry in target_index_list
    # a value of 1 will be recorded
    for index in target_index_list:
        data[indicator_name].loc[data.index.get_level_values(\
            index_name) == index] = 1

# Import data with "ISO_Code" and "Year" as index columns
data = pd.read_csv("fraserDataWithRGDPPC.csv", index_col = ["ISO_Code", "Year"], 
                   parse_dates = True)

# select "ISO_Code" from names of double index
index_name = data.index.names[0]
indicator_name = "North America"
# Cuba, Grenada, Saint Kitts, Saint Lucia, Saint Vincent are missing 
# from Fraser Data
countries_in_north_america = ["BHS", "BRB", "BLZ", "CAN", "CRI", "DOM", "SLV",
                              "GTM", "HTI", "HND", "JAM", "MEX", "NIC", "PAN",
                              "TTO", "USA"]
create_indicator_variable(data = data, indicator_name = indicator_name,
    index_name = index_name, target_index_list = countries_in_north_america)