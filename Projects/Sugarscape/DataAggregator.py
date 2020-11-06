# dataAggregator.py
import pandas as pd
from chest import *
import os
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
        
    def saveData(self, name, run):
        dict_of_chests = self.trial_data[name][run]
        pd.DataFrame(data = dict_of_chests.values(), index = dict_of_chests.keys()).T.to_csv(name.replace(":", " ") + str(run) + ".csv")