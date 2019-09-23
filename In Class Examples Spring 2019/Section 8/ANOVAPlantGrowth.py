import pandas as pd
from scipy import stats
#From https://www.marsja.se/four-ways-to-conduct-one-way-anovas-using-python/

datafile = "PlantGrowth.csv"
data = pd.read_csv(datafile, index_col = [0])
 
#Create a boxplot
data.boxplot('weight', by='group', figsize=(12, 8))
 
ctrl = data['weight'][data.group == 'ctrl']
 
grps = pd.unique(data.group.values)
d_data = {grp:data['weight'][data.group == grp] for grp in grps}
 
k = len(pd.unique(data.group))  # number of conditions
N = len(data.values)  # conditions times participants
n = data.groupby('group').size()[0] #Participants in each condition

F, p = stats.f_oneway(d_data['ctrl'], d_data['trt1'], d_data['trt2'])

DFbetween = k - 1
DFwithin = N - k
DFtotal = N - 1

