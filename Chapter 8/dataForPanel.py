#dataForPanel.py
import numpy as np
import pandas as pd

#make sure dates are imported in the same format; to do this,
#we turned off parse_dates
fraserData = pd.read_excel("EFW2018ForPython.xlsx",
                           sheet_name = "EFW Index 2018 Report",
                           index_col = [1, 0],
                           parse_dates=False)
#drop empy columns and rows
fraserData = fraserData.dropna(axis=0, thresh=1).dropna(axis=1, thresh=1)

#utf-8 error usually corrected by passing encoding='iso-8859-1'
maddisonData = pd.read_excel("mpd2018.xlsx",encoding='iso-8859-1',
                                       sheet_name = "Full data", 
                                       index_col = [0, 2])

# for loop iterates through the index keys
fraserData["RGDP Per Capita"] = maddisonData["cgdppc"]

print(fraserData["RGDP Per Capita"])
fraserData.to_csv("fraserDataWithRGDPPC.csv")