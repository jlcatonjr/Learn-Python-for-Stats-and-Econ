from tkinter import *
from Model import *
import time
class GUI():
    def __init__(self, parent, num_agents, live_visual, every_t_frames):
        self.parent = parent
        self.model = Model(self, num_agents)
        self.dimPatch = 16
        self.live_visual = live_visual
        self.every_t_frames = every_t_frames

        canvasWidth = self.model.cols * self.dimPatch
        canvasHeight= self.model.rows * self.dimPatch
        self.canvas = Canvas(parent, width=canvasWidth, height=canvasHeight, background="white")
        #puts in canvas window
        self.canvas.pack()
        if self.live_visual:
            self.drawPatches()
            
            for ID, a in self.model.agent_dict.items():
                self.drawAgent(a)
            self.canvas.update()
            
    def drawPatches(self):
        for i in self.model.patch_dict:
            for patch in self.model.patch_dict[i].values():    
                # print(patch.row, patch.col, patch.Q)                
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
 					width=0 #Border width = 0
				)
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
# 

for num_agents in range(100,1001,100):
    parent = Tk()
    parent.title = "Sugarscape"
    # num_agents = 300
    periods = 1000
    start = time.time()
    y = GUI(parent, num_agents, live_visual = False, every_t_frames = 1)
    y.model.runModel(periods)
    y.parent.quit()
    y.parent.destroy()
    end = time.time()
    elapse = end - start
    
    print("agents", "periods", "time", sep = "\t")
    print(num_agents, periods, elapse, sep = "\t")
    
if __name__ == "__main__":
    parent.mainloop()