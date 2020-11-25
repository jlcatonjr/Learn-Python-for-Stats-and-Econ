from tkinter import *
from Model import *
from DataAggregator import *
import time
import os
import gc

class GUI():
    def __init__(self, name, run, num_agents, live_visual, every_t_frames, 
                 mutate = False, genetic = False, data_aggregator=None):
        if live_visual:
            self.parent = Tk()
        self.name = name
        self.run = run
        self.live_visual = live_visual
        self.model = Model(self, num_agents, mutate, genetic, data_aggregator, live_visual)
        self.dimPatch = 16
        self.every_t_frames = every_t_frames

        canvasWidth = self.model.cols * self.dimPatch
        canvasHeight= self.model.rows * self.dimPatch
        if self.live_visual:
            self.canvas = Canvas(self.parent, width=canvasWidth, height=canvasHeight, background="white")
            #puts in canvas window
            self.canvas.pack()
            self.drawPatches()
            
            for ID, a in self.model.agent_dict.items():
                self.drawAgent(a)
            self.canvas.update()
            
    def drawPatches(self):
        for i in self.model.patch_dict:
            for patch in self.model.patch_dict[i].values():    
                patch.image = self.canvas.create_rectangle(
                            #left x                     
 					patch.col * self.dimPatch,
                            #top y
 					patch.row * self.dimPatch,
                            #right x
 					(patch.col + 1) * self.dimPatch,
                            #bottom y
 					(patch.row + 1) * self.dimPatch,
 					fill=self.color(patch.Q - 1, patch.good),
 					width=0) #Border width = 0
                
    def drawAgent(self, agent):
        agent.image = self.canvas.create_oval(
 			agent.col * self.dimPatch + 2,
 			agent.row * self.dimPatch + 2,
 			(agent.col + 1) * self.dimPatch - 2,
 			(agent.row + 1)* self.dimPatch - 2,
 			fill='red',
 			width=0
		)

    def moveAgents(self):   
        for agent in self.model.agent_dict.values():
            self.canvas.move(agent.image, 
 			agent.dx * self.dimPatch,
 			agent.dy * self.dimPatch)
            color, outline = self.agentColor(agent)
            self.canvas.itemconfig(agent.image,
                                   fill = color,
                                   outline = outline, 
                                   width = 2)
    
    def agentColor(self, agent):
        if agent.basic:
            color = "red"
        if agent.switcher:
            color = "orange"
        if agent.arbitrageur:
            color = "green"
        outline = "black" if agent.herder else color
        return color, outline
    
    def updatePatches(self):
        for i in self.model.patch_dict:
            for patch in self.model.patch_dict[i].values():    
                self.canvas.itemconfig(patch.image, fill=self.color(patch.Q, 
                                                                    patch.good))
        
    #Outputs string in the format '#RRGGBB'
    def color(self, q, good):
        #(256 / 4) - 1  = 63
        rgb = (255 - 3 * q,255 - 10 * q,255 - 51*q) if good == "sugar" else (30 - 3 * q, 50 - 5 * q ,255 - 35*q)
        color = '#'
        for v in rgb:
            # cuts off beginning of hex() output: '0x' 
            hx = hex(v)[2:]
            while len(hx) < 2: 
                # add 0 to beginning if 1 characters
                hx = '0' + hx
            color += hx
        return color


agent_attributes = ["water", "sugar", "wealth", "basic", "switcher",
                        "herder", "arbitrageur"]
model_attributes = ["population", "total_agents_created", "total_exchanges", "average_price"]

data_agg = DataAggregator(agent_attributes, model_attributes)
for mutate in [True]:
    for genetic in [True]:#(True, False):
        name = "mutate: " + str(mutate) + " genetic: " + str(genetic)
        data_agg.prepSetting(name)
        print("mutate", "genetic", sep = "\t")
        print(mutate, genetic, sep = "\t")
        print("trial", "agents", "periods", "time", sep = "\t")
        for run in range(100):
            gc.set_threshold(0,0)
            data_agg.prepRun(name, run)
            # parent.title"Sugarscape"
            num_agents = 500
            periods = 150000
            start = time.time()
            y = GUI(name, run, num_agents, live_visual = False, 
                    every_t_frames = periods, mutate = mutate, genetic = genetic,
                    data_aggregator = data_agg)
            y.model.runModel(periods, data_agg)
            # final_num_agents = len(y.model.agent_dict)
            if y.live_visual:
                y.parent.quit()
                y.parent.destroy()
            end = time.time()
            elapse = end - start
            print(run, num_agents, periods, elapse, 
                  sep = "\t")
        data_agg.saveDistributionByPeriod(name)
        data_agg.plotDistributionByPeriod(name)

# if __name__ == "__main__":
#     parent.mainloop()
