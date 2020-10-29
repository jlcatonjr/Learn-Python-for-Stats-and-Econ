import random
#Agent.py

class Agent():
    def __init__(self, model, row, col, ID):
        self.model = model
        # allocate each .good to agent within quantity in range specified by 
        # self.model.good_params
        self.good = {good :random.randint(vals["min"], vals["max"])
                     for good, vals in self.model.goods_params.items()}
        # randomly choose initial target good
        goods = list(self.good.keys())
        num_goods = len(goods)
        target_index = random.randint(0, num_goods-1)
        self.target = goods[target_index]
        del goods[target_index]
        self.not_target = goods[0]
        self.col = col
        self.row = row 
        self.dx = 0
        self.dy = 0
        self.id = ID
        self.vision = random.randint(1, self.model.max_vision )
        