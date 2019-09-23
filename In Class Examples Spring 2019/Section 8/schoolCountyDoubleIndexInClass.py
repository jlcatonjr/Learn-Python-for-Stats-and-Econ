import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

data = pd.read_csv("schoolDataRealExpenditures.csv", 
                   index_col = ["County","Year"])

county_index = data.index.get_level_values('County')
year_index = data.index.get_level_values('Year')
county_index = set(county_index)
year_index = set(year_index)
county_index = sorted(list(county_index))
year_index = sorted(list(year_index))

williams_index = data.index.get_level_values("County") == "Williams"
williams_data = data[williams_index]
williams_data.to_csv("williamsData.csv")

y2000_index = data.index.get_level_values("Year") == 2000
y2000_data = data[y2000_index]
y2000_data.to_csv("2000Data.csv")

county_folder = "County"
year_folder = "Year"
try:
    os.mkdir(county_folder)
except:
    print("Folder", county_folder, "already exists")

try:
    os.mkdir(year_folder)
except:
    print("Folder", year_folder, year_folder)

for county in county_index:
   index_for_county =  data.index.get_level_values("County") == county
   data_for_county = data[index_for_county]
   data_for_county.to_csv(county_folder + "/" + county + ".csv")

for year in year_index:
   index_for_year = data.index.get_level_values("Year") == year
   data_for_year = data[index_for_year]
   data_for_year.to_csv(year_folder + "/" + str(year) + ".csv")


pp = PdfPages("NDSchoolDataVisualizations.pdf")
for county in county_index: 
   index_for_county =  data.index.get_level_values("County") == county
   data_for_county = data[index_for_county]
   df = data_for_county.reset_index().set_index("Year")
   try:
       xname = "Total Expenditures"
       yname = "Students Enrolled / Population"
       fig, ax = plt.subplots(figsize = (15, 8))
       scatter = ax.scatter(x=df[xname],
                            y=df[yname],
                            c = df.index.get_level_values("Year"))
#       
       plt.colorbar(scatter)     
       # Axis manipulation
       ax.tick_params(axis='x', rotation = 90)
       plt.rc('xtick',labelsize=20)
       plt.rc('ytick',labelsize=20)    
       plt.xlabel(xname, fontsize = 20)
       plt.ylabel(yname, fontsize = 20)
       
       plt.ylim(ymin = 0, ymax = df[yname].max())
       plt.title(county, fontsize = 26)
       plt.show()
       pp.savefig(fig, bbox_inches = "tight")
#       
       # Create Line Graph
       fig, ax = plt.subplots(figsize = (15, 8))
       ax2 = plt.twinx()
       df[xname].plot.line(color = "C0", ax=ax)
       df[yname].plot.line(color = "C2", ax=ax2)
       ax.set_xlabel("Year", fontsize = 20)
       ax.tick_params(axis = "x", rotation = 90)
       ax.set_ylabel(xname, fontsize = 20, color = "C0")
       ax2.set_ylabel(yname, fontsize = 20, color = "C2")
       
       # format y axis as percent
       vals = ax.get_yticks()
       ax.set_yticklabels(['{:5.2e}'.format(x) for x in vals])
       vals = ax2.get_yticks()
       ax2.set_yticklabels(['{:,.3%}'.format(x) for x in vals])
       plt.title(county, fontsize = 26)
       plt.show()
       pp.savefig(fig, bbox_inches = "tight")
       plt.close()
       
   except:
       print("NAN entries for", county)
pp.close()

                