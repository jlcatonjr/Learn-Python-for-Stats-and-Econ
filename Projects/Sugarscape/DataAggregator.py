# dataAggregator.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import math
import shelve
import os
from matplotlib.backends.backend_pdf import PdfPages
from scipy.stats.mstats import gmean

class DataAggregator():
    def __init__(self, agent_attributes, model_attributes):
        self.folder = "shelves"
        self.agent_attributes = agent_attributes
        self.model_attributes = model_attributes
        self.attributes = agent_attributes + model_attributes
        
        try:
            os.mkdir(self.folder)
        except:
            # if folder is not empty, 
            # remove all files to avoid error
            files = os.listdir(self.folder)
            for file in files:
                os.remove(self.folder + "\\" + file)
        self.trial_data = {}#shelve.open(self.folder + "\\dataAgMaster")
            
    def prepSetting(self, name):
        self.trial_data[name] = shelve.open(self.folder + "\\dataAg" + name.replace(":", "-"), writeback = True)#(path = self.folder)
    
    def prepRun(self, name, run):
        self.trial_data[name][run] = {}#shelve.open(self.folder + "\\" + name.replace(":", "-") + run)
        for attribute in self.attributes:
            self.trial_data[name][run][attribute] ={}# shelve.open(
                # self.folder + "\\" + name.replace(":", "-") + run + attribute) 
    def collectData(self, model, name, run, period):
        
        def collectAgentAttributes():
            for attribute in self.agent_attributes:
                self.trial_data[name][run][attribute][period] = []
            for ID, agent in model.agent_dict.items():
                for attribute in self.agent_attributes:
                    self.trial_data[name][run][attribute][period].append(getattr(agent, attribute))
            for attribute in self.agent_attributes:
                self.trial_data[name][run][attribute][period] =\
                    np.mean(self.trial_data[name][run][attribute][period])

        def collectModelAttributes():
            for attribute in self.model_attributes:
                self.trial_data[name][run][attribute][period] = getattr(model, attribute)
                
            
        collectAgentAttributes()
        collectModelAttributes()
    
    
    def saveRun(self, name, run, run_data):
        for attribute in run_data.keys():
            for period, val in run_data[attribute].items():
                self.trial_data[name][run][attribute][period] = val
        self.trial_data[name].sync()
            
            # print(dict(self.trial_data[name][run][attribute]))
        # print(pd.read_pickle(self.trial_data[name]))
            # print(pd.concat([pd.DataFrame(dict(pair for pair self.trial_data[name][run][attributes].items()), columns = attribute) ], axis = 1 ))
            # print(pd.DataFrame(
                # print(dict(pair for pair in self.trial_data[name][run][attribute].items())), 
                # columns = attribute))
    def saveData(self, name, trial):
        dict_of_chests = self.trial_data[name][trial]
        # pd.DataFrame(data = dict_of_chests.values(), 
        #               index = dict_of_chests.keys()).T.to_csv(
        #                   name.replace(":", " ") + str(trial) + ".csv")
    
    def saveDistributionByPeriod(self, name):

        # for attr in self.attributes
        self.distribution_dict = {name:{attr: {trial:{} for trial in self.trial_data[name]}
                                        for attr in self.attributes}}
        for attr in self.attributes:
            for trial in self.trial_data[name]:
                # for period in self.trial_data[name][trial]:
                self.distribution_dict[name][attr][trial] = self.trial_data[name][trial][attr]

    def plotDistributionByPeriod(self, name):

        def build_distribution_video(df, attr):
            def plot_curves(frame, *kwargs):
                ax.clear()
                # the FuncAnimation cycles through each frame in frames,
                ax.tick_params('both', length=0, which='both')
                ax.tick_params(axis='x', rotation=90)
                vals = ax.get_yticks()
                new_vals = [str(int(y * 100)) + "%" for y in vals]
                ax.set_yticklabels(new_vals)
    
                plot_df.loc[frame].plot.hist(bins = bins, label = frame, density = True, 
                                       ax = ax)
                # Turn the text on the x-axis so that it reads vertically
                # ax.set_xlim(left =min_x, right = max_x)
                # ax.set_ylim(bottom = 0, top = max_y)
                # ax.tick_params(axis='x', rotation=90)
                ax.set_title(attr + " at period " + str(frame))
                
            def init(*kwargs):
                # Get rid of tick lines perpendicular to the axis for aesthetic
                ax.tick_params('both', length=0, which='both')
                #plt.xticks([i for i in range(len(data.index))], list(data.index))
                ax.tick_params(axis='x', rotation=90)
                # transform y-axis values from sci notation to integers
                # ax.set_xlim(left = min_x, right = max_x)
                # ax.set_ylim(bottom = 0, top = max_y)
                vals = ax.get_yticks()
                new_vals = [str(int(y * 100)) + "%" for y in vals]
                ax.set_yticklabels(new_vals)
                
            # df.fillna(0, inplace = True)
            # start plotting after burn in period
            df_index = list(df.index)[100:]
            plot_df = df.loc[df_index]
            # min_x = plot_df.min().min()
            # max_x = plot_df.max().max()
            # max_y = plot_df.T.nunique().max() / len(df.keys())
            frames = df_index
            fig, ax = plt.subplots(figsize=(40,20))
            plt.rcParams.update({"font.size": 30})
            bins = 20
            kwargs = (plot_df, fig, ax,bins, attr)  #min_x, max_x, max_y, 
            anim = FuncAnimation(fig, plot_curves, frames = frames, 
                                 blit = False, init_func = init, interval=25, 
                                 fargs =kwargs)
            # Use the next line to save the video as an MP4.
            anim.save(attr + "Evolution.mp4", writer = "ffmpeg")
            plt.close()
        
        def build_line_plots_with_scatter(df, attr, pp, alt_x_axis = False):
            fig, ax = plt.subplots(figsize = (40, 24))

            if alt_x_axis is False:
                x_name = "period"
                for key, col in df.drop(["generations mean", "exchanges mean"], axis = 1).items():
                    ax.scatter(x = df.index, y = col, c = "C0",
                               s = 10, alpha = .2)
                df["mean"].plot.line(c="C3", linewidth = 10, ax = ax)
            else:
                x_name = alt_x_axis
                for key, col in df.drop(["generations mean", "exchanges mean"], axis = 1).items():
                    ax.scatter(x = df[alt_x_axis], y = col, c = "C0",
                               s = 5, alpha = .2)
                ax.plot(df[alt_x_axis], df["mean"], c="C3", 
                        linewidth = 10)
                
            ax.set_xlabel(x_name)
            
            ax.set_title(attr.replace("_", " ").title(), fontsize= 50)
            folder = "plots"
            try:
                os.mkdir(folder)
            except:
                pass
            
            if pp != None: pp.savefig(fig, bbox_inches = "tight")  
            plt.savefig(folder + "\\" + attr +"x=" + x_name + "linxliny.png")
            ax.set_xscale("log")
            if pp != None: pp.savefig(fig, bbox_inches = "tight")  
            plt.savefig(folder + "\\" +attr + "x=" + x_name + "logxliny.png")
            ax.set_yscale("log")
            if pp != None: pp.savefig(fig, bbox_inches = "tight")  
            plt.savefig(folder + "\\" +attr+"x=" + x_name + "logxlogy.png")
            ax.set_xscale("linear")
            if pp != None: pp.savefig(fig, bbox_inches = "tight")  
            plt.savefig(folder + "\\" +attr+"x=" + x_name + "linxlogy.png")
            plt.close()
        plt.rcParams.update({"font.size": 30})
        pp = None# PdfPages("Sugarscape Plots.pdf")
        
        gen_dict = self.distribution_dict[name]["total_agents_created"]
        gen_df = pd.DataFrame(data = gen_dict.values(), 
                          index= gen_dict.keys()).T
        gen_df.index = gen_df.index.astype(int)
        gen_df = gen_df.sort_index()
        gen_df.index.name = "Number of Generations"
        gen_df["mean"] = gen_df.mean(axis = 1)
        
        exchange_dict = self.distribution_dict[name]["total_exchanges"]
        exchange_df = pd.DataFrame(data = exchange_dict.values(), 
                          index= exchange_dict.keys()).T
        exchange_df.index = exchange_df.index.astype(int)
        exchange_df = exchange_df.sort_index()
        exchange_df.index.name = "Cumulative Exchanges"
        exchange_df["mean"] = exchange_df.mean(axis = 1)
        
        for name in self.distribution_dict:
            for attr in self.distribution_dict[name]:
                for trial in self.distribution_dict[name][attr]:
                    dict_of_chests = self.distribution_dict[name][attr]
                df = pd.DataFrame(data = dict_of_chests.values(), 
                                  index= dict_of_chests.keys()).T
                df.index = df.index.astype(int)
                df = df.sort_index()
                # build_distribution_video(df, attr)
                if attr != "average_price":
                    df["mean"] = df.mean(axis=1)
                else:
                    df["mean"] = [gmean(df.loc[row].dropna()) for row in df.index]
                
                df["generations mean"] = gen_df["mean"]
                df["exchanges mean"] = exchange_df["mean"]
                build_line_plots_with_scatter(df, attr, pp = pp)
                build_line_plots_with_scatter(df, attr, pp = pp, alt_x_axis = "generations mean")
                build_line_plots_with_scatter(df, attr, pp = pp, alt_x_axis = "exchanges mean")                
                # else:
                #     df["mean"] = np.nan
                #     for row in df.index
                #     df.loc[row]["mean"] = gmean(df.drop("mean").loc["row"])
                    
                    
        if pp != None: pp.close()
    def remove_shelves(self):
        def process_files(path):
            files = os.listdir(path)
            for file in files:
                if ".dat" in file or ".dir" in file or ".bak" in file:
                    os.remove(path + "\\" + file)
        path = self.folder
        process_files(path)
        path = "."
        process_files(path)