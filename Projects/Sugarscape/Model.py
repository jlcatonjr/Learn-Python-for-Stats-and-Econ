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
        self.min_init_sugar = 5
        self.max_init_sugar = 25
        self.max_vision = 1
        # hash table that identifies possible moves relative to agent position 
        self.move_dict = {
            v:{
                i:{
                    j: True for j in range(-v, v + 1) if (i ** 2 + j ** 2) <= (v ** 2) }
                for i in range(-v, v + 1)}
            for v in range(1, self.max_vision + 1)}
        # {i:{j:{k:""}} for i in range(10) for j in range(10) for k in range(10)}
        # {i:{j:{k: i * j * k for k in range(5) if k < 3} for j in range(2)} for i in range(2) }
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
        
    def initializePatches(self):
        #Instantiate Patches
        #Create a list to hold the patches. We first fill these with
        #zeros to hold the place for each Patch object
        self.patch_dict = {i:{j:0} for i in range(self.rows) for j in range(self.cols)}
        for i in range(self.rows):
            for j in range(self.cols):
                #replace zeros with actual Patch objects
                self.patch_dict[i][j] = Patch(self,  i , j, self.sugarMap[i][j], "sugar")
        self.empty_patches = RandomDict({(i,j):self.patch_dict[i][j] for i in range(self.rows) for j in range(self.cols)})
                
        
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
        for period in range(periods):
            # print("period:", period)
            self.growPatches()
            random.shuffle(agent_list)
            for agent in agent_list:
                self.agentMove(agent)
            # if period % 1 == 0:
            #     self.GUI.updatePatches()
            #     self.GUI.moveAgents()
            #     self.GUI.canvas.update()
            
    def agentMove(self, agent):
        max_patch = {"sugar":None,
                     "water":None}
        max_q = {"sugar":0,
                 "water":0}
        curr_i, curr_j = agent.row, agent.col
        
        patch_moves = [(curr_i + i, curr_j + j)
                       for i in self.move_dict[agent.vision]
                       for j in self.move_dict[agent.vision][i]]
        random.shuffle(patch_moves)
        near_empty_patch = False
        for i in range(len(patch_moves)):
                            
            coords = patch_moves[i]
            if coords in self.empty_patches:
                near_empty_patch = True
                i, j = coords[0], coords[1]                            
                empty_patch = self.patch_dict[i][j]
                patch_q = empty_patch.Q
                patch_good = empty_patch.good
                if patch_q > max_q[patch_good]:
                    max_patch[patch_good] = empty_patch
                near_empty_patch = True
                
        if near_empty_patch:
            # agent_move()
            target_patch = max_patch[agent.target]
            new_coords = target_patch.row, target_patch.col                
            agent.dx = target_patch.col - agent.col
            agent.dy = target_patch.row - agent.row
            agent.row, agent.col = new_coords
            del self.empty_patches[new_coords]
            self.empty_patches[curr_i, curr_j] = self.patch_dict[curr_i][curr_j]
        else:
            agent.dx = 0
            agent.dy = 0
        # agent_harvest()
        agent_patch = self.patch_dict[agent.row][agent.col]
        agent.good[agent_patch.good] += agent_patch.Q
        agent_patch.Q = 0 

    
    def growPatches(self):
        for i, vals in self.patch_dict.items():
            for patch in vals.values():
                if patch.Q < patch.maxQ:
                    patch.Q += 1