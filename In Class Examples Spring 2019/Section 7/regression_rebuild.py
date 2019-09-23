#regression.py
import pandas as pd
import copy
from stats import *

class Regression:
    def __init__(self):
        self.stats = Stats()

    def regress(self, reg_name, data, y_name, beta_names, min_value = 0,
                max_val = None, constant = True):
        self.min_val =  0
        if max_val != None:
            self.max_val = max_val
        else:
            self.max_val = len(data)
        self.reg_name = reg_name
        self.data = copy.copy(data)
        if constant:
            self.add_constant()
            self.beta_names.append("Constant")
        self.y_name = y_name
        self.beta_names = copy.copy(beta_names)
        
    def add_constant(self):
        self.data["Constant"] = 1
        self.beta_names.append("Constant")