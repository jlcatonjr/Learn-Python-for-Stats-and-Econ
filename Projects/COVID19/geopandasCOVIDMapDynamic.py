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

def create_covid_geo_dataframe(covid_data, map_data, dates):
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



def select_data_within_bounds(data, minx, miny, maxx, maxy):
    data = data[data.bounds["maxx"] <= maxx]
    data = data[data.bounds["maxy"] <= maxy]
    data = data[data.bounds["minx"] >= minx]
    data = data[data.bounds["miny"] >= miny]
    
    return data


def plot_map(i, *fargs):
    ax.clear()
    date = dates[i]
    print(date)
    cmap = cm.get_cmap('Reds', 4)
    if log:
        norm = cm.colors.LogNorm(vmin=vmin, vmax =vmax)
    else:
        norm = cm.colors.Normalize(vmin = vmin, vmax = vmax)
    plt.cm.ScalarMappable(cmap=cmap, norm=norm)#round(vmax, len(str(vmax))-1)))
    plot_df = df[df.index.get_level_values("date")==date]
    plot_df.plot(ax=ax, cax = ax, column=key, vmin=vmin ,vmax = vmax, 
                 cmap = cmap, legend=False, linewidth=.5, edgecolor='lightgrey', 
                 norm = norm)
    ax.set_title(str(date)[:10] + "\n" + "COVID-19 in the U.S.", fontsize = 30)
    
def init(*fargs):
    # Create colorbar as a legend
    cmap = cm.get_cmap('Reds', 4)
    print(vmin, vmax)
    
    if log:
        norm = cm.colors.LogNorm(vmin = vmin, vmax = vmax)
    else:
        norm = cm.colors.Normalize(vmin = vmin, vmax = vmax)
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    # empty array for the data range
    sm._A = []
    # add the colorbar to the figure
    divider = make_axes_locatable(ax)
    size = "5%" 
    cax = divider.append_axes("right", size = size, pad = 0.1)
    cbar = fig.colorbar(sm, cax=cax, cmap = cmap)
    cbar.ax.tick_params(labelsize=18)
    vals = list(cbar.ax.get_yticks())
    vals.append(vmax)
    print(vals)
    if log:
        cbar.ax.yaxis.set_major_formatter(mtick.LogFormatter())
    else:
        cbar.ax.yaxis.set_major_formatter(mtick.Formatter())

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
    dates = sorted(list(set(covid_data.index.get_level_values("date"))))
    # and will be used later
    covid_data = create_covid_geo_dataframe(covid_data, map_data, dates)
    moving_average_days = 7
    create_new_vars(covid_data, moving_average_days)
    # once data is processed, it is saved in the memory
    # the if statement at the top of this block of code instructs the computer
    # not to repeat these operations 
    
    data_processed = True
dates = dates[13 * 7 * -1 - 1::7]
keys = ["Cases per Million", "Deaths per Million", 
        "Daily Cases per Million MA", "Daily Deaths per Million MA"]

if "map_bounded" not in locals():
    minx = -127
    miny = 23
    maxx = -58
    maxy = 54
    covid_map_data = select_data_within_bounds(covid_data, minx, miny, maxx, maxy)
    map_bounded = True


for key in keys:
    log = False if "Daily" in key else True
    df = covid_map_data
    vmin = 1
    vmax = df[key][df.index.get_level_values("date").isin(dates)].max()
    fig, ax = plt.subplots(figsize=(18,8),
        subplot_kw = {'aspect': 'equal'})   
    plt.rcParams.update({"font.size": 30})
    plt.xticks(fontsize = 25)
    plt.yticks(fontsize = 25)
    # the functions will unpack the tuple. The same names variable names
    # are used in the function
    kwargs = (df, key, log, dates, fig, ax, vmin, vmax)
    frames=[i for i in range(len(dates))]
    anim = FuncAnimation(fig, plot_map, frames = frames, 
                         blit = False, init_func = init, interval=750, 
                         fargs = kwargs)
    anim.save(key + ".mp4", writer = "ffmpeg")
    # with open(key.replace("/", "-")+ ".html", "w") as f:
    #     print(anim.to_html5_video(), file=f)
    plt.show()    
    plt.close()
