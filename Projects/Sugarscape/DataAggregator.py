# dataAggregator.py
import pandas as pd
from chest import *
class DataAggregator():
    def __init__(self, agent_attributes, model_attributes):
        self.agent_attributes = agent_attributes
        self.model_attributes = model_attributes
        self.attributes = agent_attributes + model_attributes
        self.trial_data = {}
        
        self.folder = "chestData"
        try:
            os.mkdir(folder)
        except:
            pass
        
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
        
    def showData(self, name, run):
        chest = self.trial_data[name][run]
        print(pd.DataFrame(data = chest.values(), index = chest.keys()).T)