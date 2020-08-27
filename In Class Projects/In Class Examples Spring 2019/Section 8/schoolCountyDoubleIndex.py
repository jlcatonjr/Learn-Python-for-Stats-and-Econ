import pandas as pd
import numpy as np
import os

data = pd.read_csv("schoolDataRealExpenditures.csv", index_col = ["County", "Year"])

county_index = data.index.get_level_values('County')
year_index = data.index.get_level_values('Year')
county_index = set(county_index)
year_index = set(year_index)
county_index = sorted(list(county_index))
year_index = sorted(list(year_index))
print(county_index)
print(year_index)


williams_index = data.index.get_level_values('County')=="Williams"
williams_data = data[williams_index]



print(williams_index)
print(williams_data)

cass_index = data.index.get_level_values('County')=="Cass"
cass_data = data[cass_index]

print(cass_data)

y2000_index = data.index.get_level_values("Year")==2000
y2000_data = data[y2000_index]
print(y2000_data)

county_folder = "County CSVs"
year_folder = "Year CSVs"
try:
    os.mkdir(county_folder)
except:
    print("Folder, " + county_folder + ", already exists")
    
try:
    os.mkdir(year_folder)
except:
    print("Folder, " + year_folder + ", already exists")
    
for county in county_index:
    index_for_county = data.index.get_level_values('County')== county
    data_for_county = data[index_for_county]
    data_for_county.to_csv(county_folder + "/" + county + ".csv")
    print(county + ".csv saved")

for year in year_index:
    index_for_year = data.index.get_level_values("Year") == year
    data_for_year = data[index_for_year]
    data_for_year.to_csv(year_folder + "/" + str(year) + ".csv")
    print(str(year) + ".csv saved")