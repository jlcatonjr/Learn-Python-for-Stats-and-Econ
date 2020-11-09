# dataAggregator.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt 
from matplotlib.animation import FuncAnimation
import math
from chest import *
import os
from matplotlib.backends.backend_pdf import PdfPages

class DataAggregator():
    def __init__(self, agent_attributes, model_attributes):
        self.agent_attributes = agent_attributes
        self.model_attributes = model_attributes
        self.attributes = agent_attributes + model_attributes
        self.trial_data = {}
        
        self.folder = "chests"
        try:
            os.mkdir(self.folder)
        except:
            # if folder is not empty, 
            # remove all files to avoid error
            files = os.listdir(self.folder)
            for file in files:
                os.remove(self.folder + "\\" + file)
            
    def prepSetting(self, name):
        self.trial_data[name] = {}
    
    def prepRun(self, name, run):
        self.trial_data[name][run] = {attribute: Chest(path = self.folder) for attribute in self.attributes}
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
        
    def saveData(self, name, trial):
        dict_of_chests = self.trial_data[name][trial]
        pd.DataFrame(data = dict_of_chests.values(), 
                     index = dict_of_chests.keys()).T.to_csv(
                         name.replace(":", " ") + str(trial) + ".csv")
    
    def saveDistributionByPeriod(self, name):

        # for attr in self.attributes
        self.distribution_dict = {name:{attr: {trial:{} for trial in self.trial_data[name]}
                                        for attr in self.attributes}}
        for attr in self.attributes:
            for trial in self.trial_data[name]:
                # for period in self.trial_data[name][trial]:
                self.distribution_dict[name][attr][trial] = self. trial_data[name][trial][attr]

    def plotDistributionByPeriod(self, name):
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


        for name in self.distribution_dict:
            for attr in self.distribution_dict[name]:
                for trial in self.distribution_dict[name][attr]:
                    dict_of_chests = self.distribution_dict[name][attr]
                df = pd.DataFrame(data = dict_of_chests.values(), 
                                  index= dict_of_chests.keys()).T
                print(df)
                df.fillna(0, inplace = True)
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

            