import numpy as np 
import pandas as pd
from scipy.stats.mstats import gmean
import random
import math
from randomdict import RandomDict
# from chest import *
import shelve
from Patch import *
from AgentBranch import *
import gc
from memory_profiler import memory_usage
import time
#Model.py
class Model():
    def __init__(self, gui, num_agents, mutate, genetic, live_visual, agent_attributes,
                 model_attributes):
        if live_visual:
            self.GUI = gui
        self.live_visual = live_visual
        self.name = gui.name
        self.run = gui.run
        self.initial_population = num_agents
        self.mutate = mutate
        self.genetic = genetic
        self.agent_attributes = agent_attributes
        self.model_attributes = model_attributes
        self.attributes = agent_attributes + model_attributes
        # attributes that are not copied during mutation or herding
        self.drop_attr = ["col", "row", "dx", "dy", "id", "wealth", "top_wealth",
            "sugar", "water","target", "not_target",
            "exchange_target", "not_exchange_target", "parent", "image"]
        # if self.GUI.live_visual:
        #     self.drop_attr.append("image")
        if self.mutate:
            self.max_mutate_rate = 0.5 if mutate else 0 #.5
        if self.genetic:
            self.cross_over_rate = .5
        ############    set model parameters    ############
        self.total_agents_created = 0   
        self.goods = ["sugar", "water"]
        self.goods_params = {good:{"min":5,
                                   "max":25} for good in self.goods}
        
        self.max_init_demand_vals = {"price":{"min": 1/2,
                                              "max": 2},
                                     "quantity":{"min":10,
                                                 "max":25}}
        self.consumption_rate = {"sugar":.5,
                                 "water":.5}
        self.primary_breeds = ["basic", "switcher", "arbitrageur"]
        self.secondary_breeds = ["herder"]
        
        self.breeds = self.primary_breeds + self.secondary_breeds
        # all agents start as basic, only mutation can create other agents
        basic = 1
        self.breed_probabilities = {"basic":basic, # if you are not a basic, you are a switcher
                                    "herder":0,
                                    "arbitrageur":0}
        self.max_vision = 1
        # record price of every transaction
        # then take average at end of period
        self.transaction_prices = []
        self.average_price = np.nan
        self.total_exchanges = 0
        ############ import map and build nav_dict ############
        # hash table that identifies possible moves relative to agent position 
        self.nav_dict = {
            v:{
                i:{
                    j: True for j in range(-v, v + 1) if 0 < (i ** 2 + j ** 2) <= (v ** 2)}
                for i in range(-v, v + 1)}
            for v in range(1, self.max_vision + 1)}
        #sugarMap.shape calls the a tuple with dimensions
        #of the dataframe
        self.sugarMap = pd.read_csv('sugar-map.txt', header = None, sep = ' ')
        # add 1 to each max_Val
        for key in self.sugarMap:
            self.sugarMap[key] = self.sugarMap[key].add(1)
        self.rows, self.cols = self.sugarMap.shape
        
        ############   Initialization   ############ 
        self.initializePatches()
        self.initializeAgents()
        self.data_dict = shelve.open("shelves\\masterShelve", writeback = True)
        for attribute in self.attributes:
            self.data_dict[attribute] = shelve.open("shelves\\subshelve-"+attribute, writeback = True) 
    
    def initializePatches(self):
        #Instantiate Patches
        #Create a dictionary to hold the patches, organize as grid. 
        #We first fill these with zeros as placeh holders
        self.patch_dict = {row:{col:0}
                           for row in range(self.rows) for col in range(self.cols)}
        for row in range(self.rows):
            for col in range(self.cols):
                # replace zeros with actual Patch objects
                good = "sugar" if row + col < self.cols else "water"
                self.patch_dict[row][col] = Patch(self,  row , col, 
                                              self.sugarMap[row][col], good)
    # use RandomDict - O(n) time complexity - for choosing random empty patch
        self.empty_patches = RandomDict({
            (row,col):self.patch_dict[row][col]
            for row in range(self.rows) for col in range(self.cols)})
        
    def initializeAgents(self):
        # agents stored in a dict by ID
        self.agent_dict = {} #if self.live_visual else Chest(path = data_aggregator.folder) #shelve.open("agent_dict") 
        # dead agents will be removed from agent_dict
        for i in range(self.initial_population):
            self.total_agents_created += 1
            ID = self.total_agents_created
            row, col = self.chooseRandomEmptyPatch()  
            self.agent_dict[ID] = Agent(self, row, col, ID)
            self.patch_dict[row][col].agent = self.agent_dict[ID]
        self.population = self.total_agents_created
#     def recordAgentLocationInDict(self, agent):
#         patchIndex = self.convert2dTo1d(agent.row, agent.col)
#         self.agentLocationDict[patchIndex] = agent

    def chooseRandomEmptyPatch(self):
        row, col = self.empty_patches.random_key() 
        del self.empty_patches[row, col]

        return row, col

    def runModel(self, periods):
        def updateModelVariables():
            self.population = len(agent_list)
            self.average_price = gmean(self.transaction_prices)
            self.transaction_prices = []
            
        for period in range(1, periods + 1):
            start = time.time()
            self.growPatches()
            agent_list = list(self.agent_dict.values())
            random.shuffle(agent_list)
            for agent in agent_list:
                agent.move()
                agent.harvest()
                agent.trade()
                agent.consume()
                agent.checkAlive()
                agent.reproduce()
                agent.updateParams()
            
            # data_aggregator.collectData(self, self.name, 
            #                                  self.run, period)
            updateModelVariables()
            self.collectData(str(period))
            
            if self.live_visual:
                if period % self.GUI.every_t_frames == 0:
                    # print("period", period, "population", self.population, sep = "\t")
                    self.GUI.parent.title("Sugarscape: " + str(period))
                    self.GUI.updatePatches()
                    self.GUI.moveAgents()
                    self.GUI.canvas.update()

            if period == periods:
                mem_usage = memory_usage(-1, interval=1)#, timeout=1)
                print(period, "end memory usage before sync//collect:", mem_usage[0], sep = "\t")
                self.data_dict.sync()
                gc.collect()
                mem_usage = memory_usage(-1, interval=1)#, timeout=1)
                print(period, "end memory usage after sync//collect:", mem_usage[0], sep = "\t")
            end = time.time()
            diff = (end - start)
            print(period, diff)
    def growPatches(self):
        for i in self.patch_dict:
            for patch in self.patch_dict[i].values():
                if patch.Q < patch.maxQ:
                    patch.Q += 1


    def collectData(self, period):
        
        def collectAgentAttributes():
            temp_dict={}
            for attribute in self.agent_attributes:
                temp_dict[attribute] = []
            for ID, agent in self.agent_dict.items():
                for attribute in self.agent_attributes:
                    temp_dict[attribute].append(getattr(agent, attribute)) 
            
            for attribute, val in temp_dict.items():
                self.data_dict[attribute][period] = np.mean(val)

        def collectModelAttributes():
            for attribute in self.model_attributes:
                self.data_dict[attribute][period] = getattr(self, attribute)
                
        collectAgentAttributes()
        collectModelAttributes()
