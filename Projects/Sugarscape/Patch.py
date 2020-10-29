#Patch.py
class Patch():
    def __init__(self, model, row, col, maxQ, good):
        #This links the patch to the model that creates the patch
        self.model = model
        self.row = row
        self.col = col
        #The maximum quantity of a good that patch can hold
        self.maxQ = maxQ
        #The current quantity of a good held by a patch
        self.Q = maxQ
        self.good = good
        # agent will be added when agents are placed on patches
        self.agent = None
