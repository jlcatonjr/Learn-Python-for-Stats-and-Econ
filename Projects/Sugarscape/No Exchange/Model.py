import pandas as pd
import random
import math
from randomdict import RandomDict

from Patch import *
from Agent import *
#Model.py
class Model():
    def __init__(self, gui, num_agents):
        self.GUI = gui
        self.initial_population = num_agents
        self.total_agents_created = 0
        self.goods_params = {"sugar":{"min":5,
                                      "max":25},
                              "water":{"min":5,
                                       "max":25}}
        
        self.max_vision = 1
        # hash table that identifies possible moves relative to agent position 
        self.move_dict = {
            v:{
                i:{
                    j: True for j in range(-v, v + 1) if (i ** 2 + j ** 2) <= (v ** 2) }
                for i in range(-v, v + 1)}
            for v in range(1, self.max_vision + 1)}

        #sugarMap.shape calls the a tuple with dimensions
        #of the dataframe
        self.sugarMap = pd.read_csv('sugar-map.txt', header = None, sep = ' ')
        # add 1 to each max_Val
        for key in self.sugarMap:
            self.sugarMap[key] = self.sugarMap[key].add(1)
        self.rows, self.cols = self.sugarMap.shape
        #Use to efficiently track which patches are empty
        self.initializePatches()
        self.initializeAgents()
        # self.aggregate_data = {"agent":}

    def initializePatches(self):
        #Instantiate Patches
        #Create a list to hold the patches. We first fill these with
        #zeros to hold the place for each Patch object
        self.patch_dict = {i:{j:0}
                           for i in range(self.rows) for j in range(self.cols)}
        for i in range(self.rows):
            for j in range(self.cols):
                #replace zeros with actual Patch objects
                good = "sugar" if i + j >= self.rows else "water"
                self.patch_dict[i][j] = Patch(self,  i , j, 
                                              self.sugarMap[i][j], good)
        self.empty_patches = RandomDict({
            (i,j):self.patch_dict[i][j]
            for i in range(self.rows) for j in range(self.cols)})
                
        
    def initializeAgents(self):
        self.agent_dict = {}
        # self.agentLocationDict = {}
        for i in range(self.initial_population):
            self.total_agents_created += 1
            ID = self.total_agents_created
            row, col = self.chooseRandomEmptyPatch()  
            del self.empty_patches[row, col]
            self.agent_dict[ID] = Agent(self, row, col, ID)
        
#     def recordAgentLocationInDict(self, agent):
#         patchIndex = self.convert2dTo1d(agent.row, agent.col)
#         self.agentLocationDict[patchIndex] = agent

    def chooseRandomEmptyPatch(self):
        i, j = self.empty_patches.random_key() 
        return i, j

    def runModel(self, periods):
        agent_list = list(self.agent_dict.values())
        for period in range(1, periods + 1):
            # print("period:", period)
            self.growPatches()
            random.shuffle(agent_list)
            for agent in agent_list:
                self.agentMove(agent)
            if self.GUI.live_visual:
                if period % self.GUI.every_t_frames == 0:
                    self.GUI.updatePatches()
                    self.GUI.moveAgents()
                    self.GUI.canvas.update()
                
    def agentMove(self, agent):
        # save agent coords to track agent movement, changes in (not) empty patches
        curr_i, curr_j = agent.row, agent.col
        max_patch, near_empty_patch = self.findMaxEmptyPatch(agent, curr_i, curr_j)
        if near_empty_patch[agent.target]:
            target = agent.target
        else:
            target = agent.not_target
        self.moveToMaxEmptyPatch(agent, curr_i, curr_j, max_patch, 
                                 near_empty_patch, target)
        self.agentHarvest(agent)

    def findMaxEmptyPatch(self, agent, curr_i, curr_j):
        # dict to save empty patch with max q for each good
        max_patch = {good:{"Q":0,
                           "patch":None}
                     for good in self.goods_params}
        
        patch_moves = [(curr_i + i, curr_j + j)
                       for i in self.move_dict[agent.vision]
                       for j in self.move_dict[agent.vision][i]]
        # shuffle patches so not movement biased in one direction
        random.shuffle(patch_moves)
        near_empty_patch = {good: False for good in self.goods_params}
        for coords in patch_moves:        
            if coords in self.empty_patches:
                i, j = coords[0], coords[1]
                empty_patch = self.patch_dict[i][j]
                patch_q = empty_patch.Q
                patch_good = empty_patch.good
                near_empty_patch[patch_good] = True
                if patch_q > max_patch[patch_good]["Q"]:
                    max_patch[patch_good]["patch"] = empty_patch
                    max_patch[patch_good]["Q"] = patch_q
        return max_patch, near_empty_patch    

    def moveToMaxEmptyPatch(self, agent, curr_i, curr_j, 
                            max_patch, near_empty_patch,
                            target):
        if near_empty_patch[target]:
            # agent_move()
            target_patch = max_patch[target]["patch"]
            new_coords = target_patch.row, target_patch.col                
            agent.dx = target_patch.col - curr_j
            agent.dy = target_patch.row - curr_i
            agent.row, agent.col = new_coords
            del self.empty_patches[new_coords]
            self.empty_patches[curr_i, curr_j] = self.patch_dict[curr_i][curr_j]
        else:
            agent.dx = 0
            agent.dy = 0
    
    def agentHarvest(self, agent):    
        agent_patch = self.patch_dict[agent.row][agent.col]
        agent.good[agent_patch.good] += agent_patch.Q
        agent_patch.Q = 0 
    
    def growPatches(self):
        for i, vals in self.patch_dict.items():
            for patch in vals.values():
                if patch.Q < patch.maxQ:
                    patch.Q += 1