# dataAggregator.py
import pandas as pd
from chest import *
import os
import matplotlib.pyplot as plt
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
        self.distribution_dict = {name: {trial:{} for trial in self.trial_data[name]}}
        for trial in self.trial_data[name]:
            # for period in self.trial_data[name][trial]:
            self.distribution_dict[name][trial] =self. trial_data[name][trial]["population"]
        
    def plotDistributionByPeriod(self, name):
        for name in self.distribution_dict:
            for trial in self.distribution_dict[name]:
                dict_of_chests = self.distribution_dict[name]
            df = pd.DataFrame(data = dict_of_chests.values(), 
                              index= dict_of_chests.keys()).T
            # start plotting after burn in period
            df_index = list(df.index)[100:]
            plot_df = df.loc[df_index]
            min_x = plot_df.min().min()
            max_x = plot_df.max().max()
            max_y = plot_df.T.count().max() / len(df.keys())
            pp = PdfPages("population" + ".pdf")
            for index in plot_df.index:
                fig, ax = plt.subplots(figsize = (24, 18))
                plot_df.loc[index].hist(bins = 20, label = index, density = True, 
                                   ax = ax)
                ax.axvline(x = plot_df.loc[index].mean(), ymin = 0, 
                           ymax = .15)
                ax.set_ylim(bottom = 0, top = .15)
                ax.set_xlim(left = min_x, right = max_x)
                ax.set_title(str(index))
                pp.savefig(fig, bbox_inches = "tight")
                plt.show()
                plt.close()
            pp.close()