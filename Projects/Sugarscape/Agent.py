import random
#Agent.py

class Agent():
    def __init__(self, model, row, col, ID):
        self.model = model
        self.good = {"sugar":random.randint(self.model.min_init_sugar, self.model.max_init_sugar),
                     "water":random.randint(self.model.min_init_sugar, self.model.max_init_sugar)}

        self.target = "sugar"
        self.col = col
        self.row = row 
        self.dx = 0
        self.dy = 0
        self.id = ID
        self.vision = random.randint(1, self.model.max_vision )
        