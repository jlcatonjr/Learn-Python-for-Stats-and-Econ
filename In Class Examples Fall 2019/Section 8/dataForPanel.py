#dataForPanel.py
import pandas as pd

# make sure dates are imported in the same format; to do this,
# we turned off parse_dates
# fraser data has empty columns and rows on top and left of the file
fraser_data = pd.read_excel("efw-2019-master-index-data-for-researchers.xlsx",
                            sheet_name = "EFW Panel Data 2019 Report",
                            header = [2], index_col = [2,1])
# drop any empty column and any empty row
# row: axis = 0
# column: axis = 1
# drop any row or column with all nan values: .dropna(. . . thresh = 1)
# drop any row or column with a single nan value: default if not identified explicitly
fraser_data = fraser_data.dropna(axis = 1, thresh = 1).dropna(axis=0)
maddison_data = pd.read_excel("mpd2018.xlsx", sheet_name = "Full data",
                              index_col = [0,2])
print(maddison_data)
fraser_data["RGDP Per Capita"] = maddison_data["cgdppc"]
fraser_data.to_csv("fraserDataWithRGDPPC.csv")