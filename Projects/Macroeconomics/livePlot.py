#%matplotlib notebook
import ipywidgets as ipw 
import numpy as np
import matplotlib.pyplot as plt

class livePlot(): 
    def __init__(self, M = 10 ** 3, V = 8, y0 = 10 ** 2 * 5):

        plt.rcParams["font.size"] = 20
        self.fig, self.ax = plt.subplots(1, figsize = (8, 6))
        
        self.maxx = 1000
        self.maxy = 130
        self.ax.set_xlim(0, self.maxx)
        self.ax.set_ylim(0, self.maxy)
        plt.xticks([])
        plt.yticks([])

        self.M = 10 ** 3
        self.V = 8

        self.y = np.linspace(1, self.M, self.M)
        self.y0 = 10 ** 2 * 5

        self.AD, = self.ax.plot(self.y, self.M * self.V / self.y)
        self.LRAS = self.ax.axvline(self.y0)

        x_int, y_int = self.get_intersect(self.AD, self.LRAS, line2_vert = True)
        self.h_line_intersect = self.ax.axhline(y_int, xmin = 0, xmax = x_int, 
                                      ls = "--", color = "k")

        self.text_vert_shift = 1
        self.text_horiz_shift = 20
        self.P_text = self.ax.text(-50, y_int, "$P$")
        self.AD_text = self.ax.text(900, self.AD.get_ydata()[900] + self.text_vert_shift * -2, "$AD$")
        self.LRAS_text = self.ax.text(self.LRAS.get_xdata(orig=False)[0] + self.text_horiz_shift ,
                                      110, "$LRAS$")
        self.y0_text = self.ax.text(self.LRAS.get_xdata(orig=False)[0] - self.text_horiz_shift * .75, -10, "$y$")
        # self.MV_val_text = self.ax.text(1001, 100, "MV =" +str(self.M * self.V))
        # self.str_vals = "MV =" +str(int(self.M * self.V)) + "   P =" + str(int(self.M * self.V / self.y0)) + "   y ="+ str(int(self.y0))
        self.show_vals = self.ax.text(1, self.maxy * 1.03, 
                                      "MV =" +str(int(self.M * self.V)) + "    P =" + str(int(self.M * self.V / self.y0)) + "    y ="+ str(int(self.y0)),
                                      fontsize = 14) 

        self.interact()
        
    def interact(self):
        def update(M = self.M, V = self.V, y0 = self.y0):
            self.AD.set_ydata(M * V / self.y)
            self.LRAS.set_xdata(y0)
            x_int, y_int = self.get_intersect(self.AD, self.LRAS, line2_vert = True)
            self.h_line_intersect.set_ydata(y_int)
            self.AD_text.set_position((900, self.AD.get_ydata()[900] + self.text_vert_shift))
            self.P_text.set_position((-50, y_int + self.text_vert_shift * -2))
            self.LRAS_text.set_position((self.LRAS.get_xdata(orig=False)[0] + self.text_horiz_shift ,
                                      110))
            self.y0_text.set_position((self.LRAS.get_xdata(orig=False)[0] - self.text_horiz_shift * .75,-10))
            # self.str_vals = "MV =" +str(int(self.M * self.V)) + "   P =" + str(int(self.M * self.V / self.y0)) + "   y ="+ str(int(self.y0))
            self.show_vals.set_text(
                "$MV=$" + "$("+ str(M) + ")(" + str(V) + ")=" + str(int(M * V)) + "$  $y ="+ str(int(y0)) + "$ $P = " + str(int(M*V)) + " / " + str(y0)+"="+ str(round(M * V / y0,1)) + "$") 
            # title = self.ax.text("MV =" +str(self.M * self.V)) 

            
        self.widget = ipw.interact(update, 
                     M = ipw.widgets.IntSlider(value=self.M,
                       min=self.M / 10,
                       max=self.M * 2,
                       step=10),
                    V = ipw.widgets.FloatSlider(value = self.V * 1.5,
                        min= self.V / 10,
                        max = self.V * 2,
                        step = .1),
                    y0 = ipw.widgets.IntSlider(values = self.y0,
                        min = self.y0 / 4,
                        max = self.y0 * 2,
                        step = 5))
        
    def get_intersect(self, line1, line2, line2_vert = False):
        if line2_vert == False:
            x = np.argwhere(np.diff(np.sign(line1 - line2))).flatten()
        else:
            line1_data = line1.get_data()
            # set orig = False or else list reads as float
            line2_xdata = line2.get_xdata(orig=False)[0]
            dist = [np.abs(i - line2_xdata) for i in line1_data[0]]
            min_dist = min(dist)
            x = dist.index(min_dist)
            y = line1_data[1][x]

        return x, y
