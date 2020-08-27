import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("unemploymentData.csv", parse_dates = True, 
                 index_col = ["DATE"])

names = ["Unemployment Rate", "Natural Rate of Unemployment"]

plt.rcParams['axes.ymargin'] = 0
plt.rcParams['axes.xmargin'] = 0

fig, ax = plt.subplots(figsize = (24,12))
ax.plot(df[names[0]], label = names[0])
ax.plot(df[names[1]], label = names[1])

# fill_between(xdata, line1data, line2data,...)
ax.fill_between(df.index, df[names[0]], df[names[1]], 
                where = df[names[1]] > df[names[0]], alpha=.1,
                color = "C0")
ax.fill_between(df.index, df[names[0]], df[names[1]], 
                where = df[names[1]] < df[names[0]], alpha=.1,
                color = "C3", label = "Cyclical Unemployment")

ax.legend(fontsize = 20)
ax.tick_params(axis='x', rotation = 90, labelsize = 25)
ax.tick_params( axis ='y', labelsize = 20)

# format y axis as percent
vals = ax.get_yticks()
ax.set_yticklabels(['{:,.0%}'.format(x) for x in vals])

plt.savefig("unemploymentData.png")
plt.show()
plt.close()
