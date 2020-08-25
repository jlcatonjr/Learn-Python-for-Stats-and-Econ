import geopandas
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import cm
import matplotlib.ticker as mtick
from matplotlib.ticker import MaxNLocator
import datetime
import datadotworld as dw

def import_geo_data(filename, index_col = "Date", rename_FIPS = "FIPS"):
    # import county level shapefile
    map_data = geopandas.read_file(filename = filename,                                   
                                   index_col = index_col)
    map_data.rename(columns={"COUNTYFP":rename_FIPS, "State":"state"},
                    inplace = True)
    map_data[rename_FIPS] = map_data["STATEFP"].astype(str) + \
        map_data[rename_FIPS].astype(str)
    map_data[rename_FIPS] = map_data[rename_FIPS].astype(np.int64)
    map_data.set_index("fips_code", inplace=True)
    cea_data = map_data.to_crs({"proj": "cea"})
    map_data["area (sq. km)"] = cea_data.area / 10 ** 6
    
    return map_data

def import_covid_data(filename, fips_name):
    # Load COVID19 county data using datadotworld API
    # Data provided by Johns Hopkins, file provided by Associated Press
    dataset = dw.load_dataset("associatedpress/johns-hopkins-coronavirus-case-tracker")
    covid_data = dataset.dataframes["2_cases_and_deaths_by_county_timeseries"]
    covid_data = covid_data[covid_data[fips_name] < 57000]
    covid_data[fips_name] = covid_data[fips_name].astype(int)
    covid_data.set_index([fips_name, "date"], inplace = True)
    covid_data.loc[:, "state_abr"] = ""
    for state, abr in state_dict.items():
        covid_data.loc[covid_data["state"] == state, "state_abr"] = abr

    return covid_data

def create_covid_geo_dataframe(covid_data, map_data):
    # create geopandas dataframe with multiindex for date
    # original geopandas dataframe had no dates, so copies of the df are 
    # stacked vertically, with a new copy for each date in the covid_data index
    #(dates is a global)
    i = 0
    for date in dates:
        df = covid_data[covid_data.index.get_level_values("date")==date]
        counties = df.index.get_level_values("fips_code")
        agg_df = map_data.loc[counties]
        agg_df["date"] = df.index.get_level_values("date")[0]
        if i == 0:
            matching_gpd = geopandas.GeoDataFrame(agg_df, crs = map_data.crs)
            i += 1
        else:
            matching_gpd = matching_gpd.append(agg_df, ignore_index = False)         
    matching_gpd.reset_index(inplace=True)
    matching_gpd.set_index(["fips_code","date"], inplace = True)
    for key, val in covid_data.items():
        matching_gpd[key] = val
    matching_gpd["Location"] = matching_gpd["NAME"] + ", " + \
        matching_gpd["state_abr"]
    return matching_gpd   
    
def create_state_dataframe(covid_data):
    states = list(state_dict.keys())
    states.remove("District of Columbia")
    
    state_data = covid_data.reset_index().set_index(["date", "state","fips_code"]).groupby(["state", "date"]).sum(numeric_only = True,
              ignore_index = False) 
    drop_cols = ["uid", "location_name", "cumulative_cases_per_100_000", 
                 "cumulative_deaths_per_100_000", "new_cases_per_100_000",
                 "new_deaths_per_100_000",'new_cases_rolling_7_day_avg', 
                 'new_deaths_rolling_7_day_avg']
    # These values will be recalculated since the sum of the county values
    # would need to be weighted to be meaningful
    state_data.drop(drop_cols, axis = 1, inplace = True)
    state_data["location_type"] = "state"
    for state in states:
        state_data.loc[state_data.index.get_level_values("state") == state, "Location"] = state
        state_data.loc[state_data.index.get_level_values("state") == state, "state_abr"] = state_dict[state]
        
    return state_data    

def create_new_vars(covid_data, moving_average_days):
#    covid_data["Population / Sq Km"] = covid_data["total_population"].div(covid_data['area (sq. km)'])
    for key in ["cases", "deaths"]:
        cap_key = key.title()
        covid_data[cap_key + " per Million"] = covid_data["cumulative_" + key].div(covid_data["total_population"]).mul(10 ** 6)
        covid_data["Daily " + cap_key + " per Million"] = \
            covid_data["cumulative_" + key ].groupby(covid_data.index.names[0])\
            .diff(1).div(covid_data["total_population"]).mul(10 ** 6)
        covid_data["Daily " + cap_key + " per Million MA"] = covid_data["Daily " + \
                  cap_key + " per Million"].rolling(moving_average_days).mean()

        
def create_zero_day_dict(covid_data, start_date):
    zero_day_dict = {}
    for key in ["Cases", "Deaths"]:
        zero_day_dict[key + " per Million"] = {}
        zero_day_dict["Daily " + key + " per Million MA"] = {}
    day_zero_val = {}
    for key in zero_day_dict:
        day_zero_val[key] = 2 if "Deaths" in key else 10
    entities = sorted(list(set(covid_data.index.get_level_values(0))))    
    for key in zero_day_dict.keys():
        vals = covid_data[key]
        thresh_vals = covid_data["Deaths per Million"] if "Deaths" in key else \
            covid_data["Cases per Million"]
        dz_val = day_zero_val[key]
        for entity in entities:
            dpc = vals[vals.index.get_level_values(0) == entity][thresh_vals > dz_val]
            dpc = dpc[dpc.index.get_level_values("date") > start_date]
            zero_day_dict[key][entity] = dpc.copy()
            print(entity)
    return zero_day_dict, day_zero_val

def plot_zero_day_data(state_name, state, covid_data, zero_day_dict, 
                       day_zero_val, keys, entity_type, entities, pp, 
                       n_largest = 10, bold_entities = None, daily = False):
    max_x = 0
    fig, a = plt.subplots(2,1, figsize = (48, 32))
    for key in keys:
        val_key = "Daily " + key + " MA" if daily else key
        if len(entities) > 0:
            i = 0
            j = 0       
            ax = a[0] if "Cases" in key else a[1]
            max_x, max_y = plot_double_lines(ax, zero_day_dict, day_zero_val, val_key, entities, daily)
            locs, top_locs = identify_plot_locs(state_name, covid_data, bold_entities) 
            
            for entity in entities:
                vals = zero_day_dict[val_key][entity]
                if len(vals) > 0 and entity != "District of Columbia":
                    loc = locs[locs.index.get_level_values(entity_type) == entity]["Location"][0]                    
                    i, j = plot_lines_and_text(ax, vals, state, state_dict, loc, 
                                        top_locs, colors_dict, i, j)
            # set plot attributes
            if daily: 
                ax.set_ylim(bottom = 0, top = max_y * 1.08)
            else:
                ax.set_yscale('log')
                if max_y is not np.nan:
                    ax.set_ylim(bottom = np.e ** (np.log(day_zero_val[key])), top = np.e ** (np.log(max_y * 4) ))
            vals = ax.get_yticks()
            ax.set_yticklabels([int(y) if y >= 1 else round(y,1) for y in vals])    
            ax.set_ylabel(val_key)

            ax.set_xlim(right = max_x + 10)
            ax.set_xlabel("Days Since " + key + " Exceeded " + str(day_zero_val[key]))
    title = str(end_date)[:10] + "\n7 Day Moving Average" + "\nCOVID-19 in " + state_name if daily else str(end_date)[:10] + "\nCOVID-19 in " + state_name
    y_pos = .987 if daily else .95
    fig.suptitle(title , y=y_pos, fontsize = 75)
   
    pp.savefig(fig, bbox_inches = "tight")
    plt.savefig("statePlots/" + state + " " + val_key + ".png", bbox_inches = "tight")
    plt.show()
    plt.close()
    
def plot_double_lines(ax, zero_day_dict, day_zero_val, key, entities, daily):
    max_x = max([len(zero_day_dict[key][entity]) for entity in entities])
    max_y = max([zero_day_dict[key][entity].max() for entity in entities]) 
    if not daily:
        double_lines ={}
        for i in [2,3,5]:
            double_lines[i] = [day_zero_val[key] * 2 ** (k/i) for k in range(9 * i)]
            ax.plot(double_lines[i], label = None, 
                     alpha = .2, color = "k",  linewidth = 5)
            ax.text(len(double_lines[i]), 
                    double_lines[i][len(double_lines[i])-1], 
                    "X2 every \n" + str(i) + " days", alpha = .2)    
        max_y2 = max(val[-1] for val in double_lines.values())
        max_y = max_y if max_y > max_y2 else max_y2
        
    return max_x, max_y

def identify_plot_locs(state_name, covid_data, bold_entities):
    if state_name == "United States": 
        locs = covid_data
        top_locs = covid_data[covid_data["state_abr"].isin(bold_entities)]
        
    else:
        locs = covid_data[covid_data["state"] == state_name][["Location", "state_abr", "total_population"]]
        top_locs = locs[locs.index.get_level_values("date")==locs.index.get_level_values("date")[0]]
        top_locs = top_locs[top_locs["total_population"] >= top_locs["total_population"].nlargest(n_largest).min()]["Location"]
    return locs, top_locs    


def plot_lines_and_text(ax, vals, state, state_dict, loc, top_locs, colors_dict, 
                        i, j):    
    def select_color(loc, top_locs, colors_dict, colors, i, j):
        val = i if loc in top_locs.values else j
        if loc not in colors_dict.keys():
            colors_dict[loc] = colors[val % 10]
        color = colors_dict[loc]
        if loc in top_locs.values: i += 1 
        else: j += 1
        return color, i, j
    color, i, j = select_color(loc, top_locs, colors_dict, colors, i, j)
    label = state_dict[loc] if state in "U.S.A." else loc[:-4].replace(" ", "\n")
    
    linewidth, ls, fontsize, alpha = (6, "-", 34, 1) if loc in top_locs.values else (2, "--", 24, .6)
    ax.plot(vals.values, label = label, 
                ls = ls, linewidth = linewidth, alpha = alpha, color = color)
    ax.text(x = len(vals.values) - 1, y = vals.values[-1], s = label, 
            fontsize = fontsize, color = color, alpha = alpha)
    return i, j



def select_data_within_bounds(data, minx, miny, maxx, maxy):
    data = data[data.bounds["maxx"] <= maxx]
    data = data[data.bounds["maxy"] <= maxy]
    data = data[data.bounds["minx"] >= minx]
    data = data[data.bounds["miny"] >= miny]
    
    return data


def plot_map(i, *fargs):
    ax.clear()
    date = dates[i]
#    cmap = cm.get_cmap('YlOrBr', 8)
    cmap = cm.get_cmap('Reds', 4)
    vmin = 1 if "Deaths" in key else 10
    print(key, date)
    
    plt.cm.ScalarMappable(cmap=cmap, norm=cm.colors.LogNorm(vmin=vmin, 
                                vmax =vmax))#round(vmax, len(str(vmax))-1)))
    plot_df = val[val.index.get_level_values("date")==date]
    plot_df.plot(ax=ax, cax = ax, column=key, vmin=vmin ,vmax = vmax, 
                 cmap = cmap, legend=False, linewidth=.5, edgecolor='lightgrey', 
                 norm = mpl.colors.LogNorm(vmin=vmin, vmax=vmax))
    ax.set_title(str(date)[:10] + "\n" + "COVID-19 in the U.S.", fontsize = 30)
    ax.axis("off")
    
def init():
    # Create colorbar as a legend
    cmap = cm.get_cmap('Reds', 4)
    vmin = 1 if "Deaths" in key else 10
    print(vmin, vmax)
    size = "5%" 
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=cm.colors.LogNorm(vmin=vmin, 
                                vmax =vmax))#round(vmax, len(str(vmax))-1)))
    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size = size, pad = 0.1)
    cbar = fig.colorbar(sm, cax=cax, cmap = cmap)
    cbar.ax.tick_params(labelsize=18)
    vals = list(cbar.ax.get_yticks())
    vals.append(vmax)
    print(vals)
    cbar.ax.yaxis.set_major_formatter(mtick.LogFormatter())
    cbar.ax.set_yticklabels([int(x) for x in vals])
    cbar.ax.set_ylabel(key, fontsize = 20)

# I maintained this dictionary to use the state abbrevations in the names of
# saved files.
state_dict = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ',
    'Arkansas': 'AR', 'California': 'CA', 'Colorado': 'CO', 'Connecticut': 'CT', 
    'Delaware': 'DE', 'District of Columbia': 'DC', 'Florida': 'FL', 
    'Georgia': 'GA', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
    'Indiana': 'IN', 'Iowa': 'IA','Kansas': 'KS', 'Kentucky': 'KY',
    'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO',
    'Montana': 'MT', 'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
    'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY', 'North Carolina': 'NC',
    'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI',
    'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX',
    'Utah': 'UT', 'Vermont': 'VT', 'Virginia': 'VA',
    'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

plt.rcParams['axes.ymargin'] = 0
plt.rcParams['axes.xmargin'] = 0
plt.rcParams.update({'font.size': 32})


if "data_processed" not in locals():
    fips_name = "fips_code"
    covid_file = "COVID19DataAP.csv"
    # rename_FIPS matches map_data FIPS with COVID19 FIPS name
    map_data = import_geo_data(filename = "countiesWithStatesAndPopulation.shp",
                    index_col = "Date", rename_FIPS = fips_name)
    covid_data = import_covid_data(filename = covid_file, fips_name = fips_name)
    # dates is global, will be called in create_covid_geo_dataframe() 
    # and will be used later
    dates = sorted(list(set(covid_data.index.get_level_values("date"))))
    covid_data = create_covid_geo_dataframe(covid_data, map_data)
    state_data = create_state_dataframe(covid_data)
    moving_average_days = 7
    create_new_vars(covid_data, moving_average_days)
    create_new_vars(state_data, moving_average_days)
    start_date = "03-15-2020"     
    end_date = dates[-1]
    county_zero_day_dict, day_zero_val = create_zero_day_dict(covid_data, start_date)    
    state_zero_day_dict, day_zero_val = create_zero_day_dict(state_data, start_date)
    # once data is processed, it is saved in the memory
    # the if statement at the top of this block of code instructs the computer
    # not to repeat these operations 
    data_processed = True

keys = ["Cases per Million", "Deaths per Million"]

lines= {}
colors = ["C" + str(i) for i in range(10)]
colors_dict = {}
pp = PdfPages("covidDataByState.pdf")
n_largest = 10


for daily in [True, False]:
    if not daily:
        for state_name, state in state_dict.items():
            state_fips = sorted(list(set(covid_data[covid_data["state_abr"] == state].index.get_level_values("fips_code").copy())))
            plot_zero_day_data(state_name, state, covid_data, county_zero_day_dict, 
                              day_zero_val, keys, "fips_code", state_fips, pp, 
                              n_largest, daily = daily)
        
    
    plot_zero_day_data("United States", "U.S.A", state_data, state_zero_day_dict, 
                      day_zero_val, keys, "state", state_dict.keys(), pp,
                          bold_entities = ["IA", "MN", "NE", "ND","SD", "WI"],
                          daily = daily)
pp.close()

if "map_bounded" not in locals():
    minx = -125
    miny = 25
    maxx = -60
    maxy = 52
    covid_map_data = select_data_within_bounds(covid_data, minx, miny, maxx, maxy)
    map_bounded = True

mpl.rcParams['animation.embed_limit'] = 200
plot_dates = sorted(list(set(covid_data[covid_data.index.get_level_values("date") > start_date].index.get_level_values("date"))))
#dates = plot_dates[plot_dates.index("2020-03-17"):]
dates = plot_dates[31*3*-1 -1::3]
keys.append("Daily Cases per Million MA")
keys.append("Daily Deaths per Million MA")
for key in keys:
    val = covid_map_data
    vmax = val[key][val.index.get_level_values("date").isin(dates)].max()
    val[key] = val[key].astype(float)
    fig, ax = plt.subplots(figsize=(18,8),
        subplot_kw = {'aspect': 'equal'})   
    plt.rcParams.update({"font.size": 30})
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    frames=[i for i in range(len(dates))]
    anim = FuncAnimation(fig, plot_map, frames = frames, 
                         blit = False, init_func = init, interval=300,
                         fargs = (ax, val, vmax, key))

    with open(key.replace("/", "-")+ ".html", "w") as f:
        print(anim.to_html5_video(), file=f)
    
    plt.close()
