#dataForPanel.py
import pandas as pd

#make sure dates are imported in the same format; to do this,
#we turned off parse_dates
fraser_data = pd.read_excel("efw-2019-master-index-data-for-researchers.xlsx",
                           sheet_name = "EFW Panel Data 2019 Report",
                           header = [2], index_col = [2, 1], parse_dates=False)
# drop any empty column and any empty row
fraser_data = fraser_data.dropna(axis=0, thresh=1).dropna(axis=1, thresh=1)

maddison_data = pd.read_excel("mpd2018.xlsx", sheet_name = "Full data", 
                              index_col = [0,2])

fraser_data["RGDP Per Capita"z] = maddison_data["cgdppc"]
fraser_data.to_csv("fraserDataWithRGDPPC.csv")