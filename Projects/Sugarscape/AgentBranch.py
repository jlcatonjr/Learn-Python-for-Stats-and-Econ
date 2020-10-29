import copy
import random
import numpy as np
from scipy.stats.mstats import gmean

#Agent.py

class Agent():
    # **inheritance are the inherited
    def __init__(self, model, row, col, ID, hasParent = False, inheritance = None):
        
        # select parameters except for row, col, ID
        
        def selectParameters(
                mutate = False, good = True, wealth = True, 
                reservation_demand = True, reproduction_criteria= True, 
                breed = True, exchange_target = True, vision = True, 
                mutate_rate = True, **mutate_kwargs):    

                        
            # at first, you are the agent does not know any one else
            # give all agents these variables to avoid error when deleted from
            # inheritance dict
            def setReservationDemand():#price_change = True, quantity_change = True):
                ### don't mutate reservation quantity and price
                ### these are set in live time
                init_vals = self.model.max_init_demand_vals
                min_res_q = init_vals["quantity"]["min"] 
                max_res_q = init_vals["quantity"]["max"] 
                min_res_p = init_vals["price"]["min"]
                max_res_p = init_vals["price"]["max"]
                self.reservation_demand = {good:{
                        "quantity": min_res_q + random.random()
                        * (max_res_q - min_res_q)}
                    for good in self.model.goods}
                self.reservation_demand["sugar"]["price"] = np.e ** (
                    np.log(min_res_p) + random.random() * (np.log(max_res_p) - np.log(min_res_p)))
                self.reservation_demand["water"]["price"] = 1 / self.reservation_demand["sugar"]["price"]
                ### set rates of adjustment
                # change price (WTP//WTA) by at most 10% per period
                # if price_change: 
                min_price_change = 1.005 if not mutate else\
                    inheritance["price_change"] / (1 + self.mutate_rate)
                max_price_change = 1.1 if not mutate else\
                    inheritance["price_change"] * (1 + self.mutate_rate)
                self.price_change =  min_price_change + random.random() * (max_price_change - min_price_change)
                # change reservation demand (quantity) by at most 10% per period
                # if quantity_change:
                min_quantity_change = 1.01 if not mutate else\
                    inheritance["quantity_change"] / (1 + self.mutate_rate)
                max_quantity_change = 1.1 if not mutate else\
                    inheritance["quantity_change"] * (1 + self.mutate_rate)
                    
                self.quantity_change = min_quantity_change + random.random() * (max_quantity_change - min_quantity_change)             
            def setReproductionLevel():
                min_reproduction_criteria, max_reproduction_criteria = {}, {}
                for good in self.model.goods:
                    min_reproduction_criteria[good] = self.model.goods_params[good]["max"] * 2 if not mutate else\
                        inheritance["reproduction_criteria"][good] / (1 + self.mutate_rate)
                    max_reproduction_criteria[good] = 2 *  min_reproduction_criteria[good] if not mutate else\
                        inheritance["reproduction_criteria"][good] * (1 + self.mutate_rate)
                self.reproduction_criteria = {
                    good :min_reproduction_criteria[good] +random.random() * (
                        max_reproduction_criteria[good] - min_reproduction_criteria[good])
                    for good in self.model.goods} 
                
            ###################################################################            

            # define mutate rate first so that it effects mutation of all
            # other attributes
            if mutate_rate and self.model.mutate:
                # Inher
                min_rate = 0 if not mutate else\
                    inheritance["mutate_rate"] / (1 + inheritance["mutate_rate"])
                max_rate = self.model.max_mutate_rate if not mutate else\
                    inheritance["mutate_rate"] * (1 + inheritance["mutate_rate"])
                # keep a hard limit on the height of mutation rate
                self.mutate_rate = min_rate + random.random() * (max_rate - min_rate)
                if self.mutate_rate <= self.model.max_mutate_rate:
                    self.mutate_rate = self.model.max_mutate_rate
               
            # set value of commodity holdings, if agent has parents,
            # these values will be replaced by the max values
            if good:
                for good, vals in self.model.goods_params.items():
                    val = random.randint(vals["min"], vals["max"])
                    setattr(self, good, val)
            
            self.wealth = sum(getattr(self, good) / self.model.consumption_rate[good]
                                         for good in self.model.goods)
            self.wealthiest = self
            self.top_wealth = wealth
                
            if reservation_demand: 
                setReservationDemand()
            if reproduction_criteria:
                setReproductionLevel()        
            # either mutate breed  or set breed for initial instance
            for breed_ in self.model.breeds:
                # if mutate, don't anchor from preselected probabilities
                # just switch select whether the breed is true or false
                if breed_ in mutate_kwargs:
                    if mutate_kwargs[breed_]:
                        select_breed = random.choice((True, False))
                        if select_breed:
                            setattr(self, breed_, select_breed)
            
            # select breed randomly if agent has no parent            
            if inheritance == None:                            
                for breed_, prob in self.model.breed_probabilities.items():
                    if random.random() <= prob :
                        setattr(self, breed_, True)  
                    else: 
                        setattr(self, breed_, False)  
                # since switcher and basic are mutually exclusive,
                # set switcher opposite of basic
            # make sure basic and switcher are not both own
            self.switcher = False if self.basic else True
            for breed_ in self.model.breeds:
                self.selectBreedParameters(breed_, mutate, inheritance, 
                                           herding = False)
            if exchange_target:
                #set exchange target randomly at first
                goods = list(self.model.goods)
                random.shuffle(goods)
                self.exchange_target = goods.pop()
                self.not_exchange_target = goods[0]
            if vision:
                    self.vision = random.randint(1, self.model.max_vision)
            # wealth is the number of periods worth of food owned by the agent
            # assumes that one good is instantly convertable to another
        
        #######################################################################
        
        def mutate():
            # select which parameters will be mutated
            mutate_dict = {key: True if random.random() < self.mutate_rate else False for key in inheritance.keys()}
            # mutate select parameters
            selectParameters(mutate = True, **mutate_dict)
            
        self.model = model
        
        if hasParent:
            ####### parameters already inerited if agent has parent ########
            for attr, val in inheritance.items():
                # print(attr, val, sep = "\n")
                setattr(self, attr, val)
            for good in self.model.goods:
                setattr(self, good, self.reproduction_criteria[good])

            # inherited values are mutated vals in dictionary if mutation is on
            if self.model.mutate:
                mutate()        
        
        else:
            selectParameters()
        self.wealth = sum(getattr(self, good) / self.model.consumption_rate[good]
                                         for good in self.model.goods)
        # allocate each .good to agent within quantity in range specified by 
        # randomly choose initial target good
        self.col = col
        self.row = row 
        self.dx = 0
        self.dy = 0
        self.id = ID
        self.reproduced = False

###############################################################################     


    def selectBreedParameters(self, breed_, mutate, inheritance, herding = False, 
                              partner = None):
        if getattr(self, breed_): 
            # those who change breed due to herding need only need to fill missing
            # parameter values
            if not herding:
                if breed_ == "basic":
                    self.target = "sugar"
                    self.not_target = "water"
                if breed_ == "switcher":
                    switch_min = 100 if not mutate or "switch_rate" not in inheritance else\
                        int(inheritance["switch_rate"] / (1 + self.mutate_rate))
                    switch_max = 1000 if not mutate or "switch_rate" not in inheritance else\
                        int(inheritance["switch_rate"] * (1 + self.mutate_rate))
                    self.switch_rate = random.randint(switch_min, switch_max) 
                    self.periods_to_switch = self.switch_rate
                    # start switcher with random target
                    goods = list(self.model.goods)
                    num_goods = len(goods)
                    target_index = random.randint(0, num_goods-1)
                    self.target = goods[target_index]
                    self.not_target = goods[0]
    
                if breed_ == "arbitrageur":
          
                    # track past exchange prices
                    # if average prices is below price agent believes is correct,
                    min_denominator = 10 if not mutate or "present_price_weight" not in inheritance else\
                        int(inheritance["present_price_weight"] / (1 + self.mutate_rate))
                    max_denominator = 100 if not mutate  or "present_price_weight" not in inheritance else\
                        int(inheritance["present_price_weight"] * (1 + self.mutate_rate))
                    self.present_price_weight = random.randint(min_denominator, max_denominator)
                    self.expected_price = self.reservation_demand["sugar"]["price"]
                    targets = copy.copy(self.model.goods)
                    random.shuffle(targets)
                    self.target = targets.pop()
                    self.not_target = targets[0]
                if breed_  == "herder":      
                    self.wealthiest = self
                    self.top_wealth = self.wealth
            else:
                if breed_  == "herder":      
                    self.top_wealth = partner.wealth
                    self.wealthiest = partner
                if breed_ == "switcher":
                    self.switch_rate = partner.switch_rate
                    self.periods_to_switch = self.switch_rate
                if breed_ == "arbitrageur":
                    self.expected_price = partner.expected_price
                    print(self.expected_price)
                print("copy breed:", breed_)
    def defineInheritance(self):
        # use attributes to define inheritance
        copy_attributes = copy.copy(vars(self))
        # redefine "good" or else values are drawn from parent for children
        # self.copy_attributes["good"] = {}
        for key in ["col", "row", "dx", "dy", "id", "wealth", "top_wealth",
                    "sugar", "water"]:
            #, "target", "exchange_target"]:#,"reservation_demand"]:
            try:
                del copy_attributes[key]
            except:
                pass 
        return copy_attributes
    
    def updateParams(self):
        def setTargetGood():
            self.wealth = sum((getattr(self,good) / self.model.consumption_rate[good] for good in self.model.goods))
            if self.switcher:
                if self.periods_to_switch == 0:
                    old_target = copy.copy(self.target)
                    new_target = copy.copy(self.not_target)
                    self.target = new_target
                    self.not_target = old_target
                    self.periods_to_switch = self.switch_rate
            if self.arbitrageur:
                # arbitrageur exchanges for the good that is cheaper than his WTP
                WTP = self.reservation_demand["sugar"]["price"]
                self.exchange_target = "sugar" if self.expected_price < WTP else "water"
            else:
                # let exchange target be determined by reservation demand
                # if shortage of both goods, choose randomly
                good1 = random.choice(self.model.goods)
                good2 = "water" if good1 == "sugar" else "sugar"
                self.exchange_target = good1 if getattr(self,good1) < self.reservation_demand[good1]["quantity"] else good2
            
        def checkReservation():
            for good in self.model.goods:
                if getattr(self, good) < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] *= self.price_change
                    self.reservation_demand[good]["quantity"] /= self.quantity_change
                if getattr(self, good) < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] /= self.price_change
                    self.reservation_demand[good]["quantity"] *= self.quantity_change
        checkReservation()
        setTargetGood()
        if self.switcher:
            self.periods_to_switch -= 1
        if self.herder:
            if self.wealthiest != self:
                # in case to level of wealth falls, as it does one population 
                # grows, allow top_wealth to decay
                self.top_wealth *= .99


    def consume(self):
        for good, rate in self.model.consumption_rate.items():
            setattr(self,good, getattr(self,good) - rate)
            
            
    
    def checkAlive(self):
        for good in self.model.goods:
            if getattr(self, good) < 0:
                self.model.dead_agent_dict[self.id] = self
                self.model.empty_patches[self.row, self.col] = self.model.patch_dict[self.row][self.col]
                if self.model.GUI.live_visual:
                    self.model.GUI.canvas.delete(self.image)
                del self.model.agent_dict[self.id]
                break
            
    def reproduce(self):
        if self.sugar > self.reproduction_criteria["sugar"] and\
            self.water > self.reproduction_criteria["water"]:
            
            # make sure inherited values are up to date
            copy_attributes = self.defineInheritance()      
            self.model.total_agents_created += 1
            row, col = self.model.chooseRandomEmptyPatch()  
            ID = self.model.total_agents_created
            self.model.agent_dict[ID] =  Agent(row=row, col=col, ID=ID, hasParent = True,  **copy_attributes)
            for good in self.model.goods:
                setattr(self, good, getattr(self,good) - self.reproduction_criteria[good])
            self.model.agent_dict[ID].top_wealth = self.wealth
            self.model.patch_dict[row][col].agent =  self.model.agent_dict[ID]
            self.model.GUI.drawAgent(self.model.agent_dict[ID])
            self.reproduced = True


######################## move method and functions ############################
    def move(self):  
        
        def findMaxEmptyPatch(curr_row, curr_col):
            # dict to save empty patch with max q for each good
            max_patch = {good:{"Q":0,
                               "patch":None}
                         for good in self.model.goods}
            
            patch_moves = [(curr_row + i, curr_col + j)  
                           for i in self.model.nav_dict[self.vision] if 0 <= curr_row + i < 50
                           for j in self.model.nav_dict[self.vision][i] if 0 <= curr_col + j < 50]
            # shuffle patches so not movement biased in one direction
            random.shuffle(patch_moves)
            near_empty_patch = False#{good: False for good in self.good}
            for coords in patch_moves:   
                if coords in self.model.empty_patches.keys:
                    empty_patch = self.model.patch_dict[coords[0]][coords[1]]
                    patch_q = empty_patch.Q
                    patch_good = empty_patch.good
                    if patch_q > max_patch[patch_good]["Q"]:
                        # only mark near empty patch if Q > 0
                        near_empty_patch = True
                        max_patch[patch_good]["patch"] = empty_patch
                        max_patch[patch_good]["Q"] = patch_q
            return max_patch, near_empty_patch    

        def moveToMaxEmptyPatch(curr_row, curr_col, 
                                max_patch, near_empty_patch,
                                target):
            
            def basicMove(max_patch):
                max_q = max(max_patch[good]["Q"] for good in max_patch )
                # include both max water and max sugar patch if moth have max_q
                max_patches = [good for good in max_patch if max_patch[good]["Q"] == max_q]
                #randomly select max water or max sugar patch
                max_good = random.choice(max_patches) 
                target_patch = max_patch[max_good]["patch"]
                return target_patch
            def chooseTargetOrAlternate(max_patch, target):
                if max_patch[target]["patch"] != None:
                    target_patch = max_patch[target]["patch"]
                else:
                    target_patch = max_patch[[good for good in self.model.goods if good != target][0]]["patch"]
                
                return target_patch
            
            ###################################################################  
            
    
            if near_empty_patch:

                if self.basic and not self.arbitrageur:
                    target_patch = basicMove(max_patch)
                else:
                    target_patch = chooseTargetOrAlternate(max_patch, target)
                # track relative position to move image
                self.dx, self.dy = target_patch.col - curr_col, target_patch.row - curr_row
                # set new coordinates
                self.row, self.col =  target_patch.row, target_patch.col 
                # register agent to patch
                self.model.patch_dict[self.row][self.col].agent = self
                # set agent at old patch to none
                self.model.patch_dict[curr_row][curr_col].agent = None
                # register old patch to empty_patches
                self.model.empty_patches[curr_row, curr_col] = self.model.patch_dict[curr_row][curr_col]
                # remove agent's current position from emtpy_patches
                del self.model.empty_patches[self.row, self.col]
            else:
                self.dx = 0
                self.dy = 0
    ###############################################################################

        # save agent coords to track agent movement, changes in (not) empty patches
        curr_row, curr_col = self.row, self.col
        max_patch, near_empty_patch = findMaxEmptyPatch(curr_row, curr_col)
        
        if near_empty_patch:
            moveToMaxEmptyPatch(curr_row, curr_col, max_patch, 
                             near_empty_patch, self.target)


    
    def harvest(self):    
        agent_patch = self.model.patch_dict[self.row][self.col]
        setattr(self, agent_patch.good, getattr(self, agent_patch.good) + agent_patch.Q)
        agent_patch.Q = 0 
        
        
    def trade(self):
        
        def askToTrade(patch):
            partner = patch.agent
            #check if partner is looking for good agent is selling
            right_good = self.exchange_target != partner.exchange_target

            return partner, right_good

        def bargain(partner):       
            WTP = self.reservation_demand[self.exchange_target]["price"] 
            WTA = partner.reservation_demand[self.exchange_target]["price"]

            # assume bargaining leads to average price...
            # maybe change to random logged distribution later
            price, can_trade = (gmean((WTA, WTP)), True) if WTP > WTA else (None, False)
            return price, can_trade
        
        def executeTrade(partner, price):
            

                
            self_res_min = self.reservation_demand[self.not_exchange_target]["quantity"]
            partner_res_min = self.reservation_demand[self.exchange_target]["quantity"]
            while (getattr(self, self.not_exchange_target) > self_res_min > price) and\
                (getattr(partner, self.exchange_target) > partner_res_min > 1):
                
                setattr(self, self.exchange_target, getattr(self, self.exchange_target) + 1)
                setattr(self, self.not_exchange_target, getattr(self, self.not_exchange_target) - price)
                setattr(partner,self.exchange_target, getattr(partner, self.exchange_target) - 1)
                setattr(partner, self.not_exchange_target, getattr(partner, self.not_exchange_target) + price)
                
                # save price of sugar or implied price of sugar for every exchange
                transaction_price = price if self.exchange_target == "sugar" else 1 / price
                self.model.transaction_prices.append(transaction_price)
                print("d")
                # record impact on arbitrageurs expected price of sugar
                if self.arbitrageur:
                    self.expected_price = (self.expected_price * (
                        self.present_price_weight) + transaction_price) / self.present_price_weight
                
        def herdTraits(agent, partner):
            if agent.herder:
                if agent.top_wealth < partner.wealth:
                    copy_attributes = partner.defineInheritance()
                    if agent.model.genetic:
                        for attr, val in copy_attributes.items():
                            if random.random() < agent.model.cross_over_rate:
                                setattr(agent, attr, getattr(partner, attr))
                                
                                if attr in self.model.breeds:                                       
                                    self.selectBreedParameters(breed_ = attr, mutate = False,
                                                               inheritance = copy_attributes,
                                                               herding = True, partner = partner)

                    else: 
                        for attr, val in copy_attributes.items():
                            setattr(agent, attr, getattr(partner, attr))
                            if attr in self.model.breeds:
                                self.selectBreedParameters(breed_ = attr, mutate = False,
                                                           inheritance = copy_attributes,
                                                           herding = True, partner = partner)
                                
    ###############################################################################            

        # find trading partner
        neighbor_patches = [(self.row + i, self.col + j)
                        for i in self.model.nav_dict[1] if 0 <= self.row + i < 50
                        for j in self.model.nav_dict[1][i] if 0 <= self.col + j < 50 ]
        random.shuffle(neighbor_patches)
        for coords in neighbor_patches:
            if coords not in self.model.empty_patches.keys:
                
                target_patch = self.model.patch_dict[coords[0]][coords[1]]
                # if partner found on patch, ask to trade
                partner, right_good = askToTrade(target_patch)
                if right_good: 
                    price, can_trade = bargain(partner)
                else:
                    price, can_trade = None, False 
                # check if partner has appropriate goods and WTP, WTA
                if can_trade:
                                        
                    # execute trades
                    executeTrade(partner, price)
                    herdTraits(self, partner)
                    herdTraits(partner, self)
                    
                    #  genetic?
                    # only trade with one partner per agent search
                    # agents can be selected by more than one partner
                    break
    


    
        
    


            
                
                
                
                
                
                
                
                
        