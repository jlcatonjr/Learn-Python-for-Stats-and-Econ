import copy
import random
import numpy as np
from scipy.stats.mstats import gmean
from Patch import *
#Agent.py

class Agent():
    # **inheritance are the inherited
    def __init__(self, model, row, col, ID, parent = None):
         
        def selectParameters(mutate = False, reservation_demand = True, 
                             reproduction_criteria= True,  
                             **mutate_kwargs):    
         
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
                ## price_change defined in kwargs if mutate
                min_price_change = 1.01 if not mutate else\
                    self.parent.price_change / (1 + self.mutate_rate)
                max_price_change = 1.1 if not mutate else\
                    self.parent.price_change * (1 + self.mutate_rate)
                self.price_change =  min_price_change + random.random() * (max_price_change - min_price_change)
                
                # change reservation demand (quantity) by at most 10% per period
                # if quantity_change:
                min_quantity_change = 1.001 if not mutate else\
                    parent.quantity_change / (1 + self.mutate_rate)
                max_quantity_change = 1.01 if not mutate else\
                    self.parent.quantity_change * (1 + self.mutate_rate)
                    
                self.quantity_change = min_quantity_change + random.random() * (max_quantity_change - min_quantity_change)             
            
            def setReproductionLevel():
                min_reproduction_criteria, max_reproduction_criteria = {}, {}
                for good in self.model.goods:
                    min_reproduction_criteria[good] = self.model.goods_params[good]["max"] * 2 if not mutate else\
                        self.parent.reproduction_criteria[good] / (1 + self.mutate_rate)
                    max_reproduction_criteria[good] = 2 *  min_reproduction_criteria[good] if not mutate else\
                        self.parent.reproduction_criteria[good] * (1 + self.mutate_rate)
                self.reproduction_criteria = {
                    good :min_reproduction_criteria[good] +random.random() * (
                        max_reproduction_criteria[good] - min_reproduction_criteria[good])
                    for good in self.model.goods} 
                
            def selectBreed():    
                if self.parent:
                    # place herder first in list
                    shuffle_breeds = copy.copy(self.model.primary_breeds)
                    random.shuffle(shuffle_breeds)
                    for breed_ in ["herder"] + shuffle_breeds:
                        if random.random() < self.mutate_rate:
                            # if mutation occurs, switch breed boolean
                            select_breed = False if getattr(self, breed_) else True
                            setattr(self, breed_, select_breed)
                            
                            if select_breed == True and breed_ in shuffle_breeds:
                                shuffle_breeds.remove(breed_)
                                for not_my_breed in shuffle_breeds:
                                    setattr(self, not_my_breed, False)
                                break
                    # set breed basic if all breeds are turned to False
                    if True not in (getattr(self, brd)
                                    for brd in self.model.primary_breeds):
                        self.setBreedBasic(herder = self.herder)

                # select breed randomly if agent has no parent            
                else:                            
                    # for breed_, prob in self.model.breed_probabilities.items():
                    #     if random.random() <= prob :
                    #         setattr(self, breed_, True)  
                    #     else: 
                    #         setattr(self, breed_, False)  
                    # since switcher and basic are mutually exclusive,
                    # All initial agents are basic, other breeds only 
                    # appear through mutation
                    self.setBreedBasic(herder = False)
                    
                self.selectBreedParameters(mutate, self.parent, 
                                           herding = False)

            def setMutateRate():
                if self.model.mutate:
                    min_rate = 0 if not mutate else\
                        self.parent.mutate_rate / (1 + self.parent.mutate_rate)
                    max_rate = self.model.max_mutate_rate if not mutate else\
                        self.parent.mutate_rate * (1 + self.parent.mutate_rate)
                    # keep a hard limit on the height of mutation rate
                    self.mutate_rate = min_rate + random.random() * (max_rate - min_rate)
                    if self.mutate_rate >= self.model.max_mutate_rate:
                        self.mutate_rate = self.model.max_mutate_rate
 



            ###################################################################            

            # define mutate rate first so that it effects mutation of all
            # other attributes
            
            setMutateRate() 
            # set value of commodity holdings, if agent has parents,
            # these values will be replaced by the max values
            setStocks()
            if reservation_demand: 
                setReservationDemand()
            if reproduction_criteria:
                setReproductionLevel()        
            setTargets()
            self.vision = random.randint(1, self.model.max_vision)
            selectBreed()
        #######################################################################

        def setStocks():
            if self.parent == None:
                for good, vals in self.model.goods_params.items():
                    val = random.randint(vals["min"], vals["max"])
                    setattr(self, good, val)
            else:
                for good in self.model.goods:
                    setattr(self, good, self.model.goods_params[good]["max"])
                    setattr(self.parent, good, 
                            getattr(self.parent,good) - self.model.goods_params[good]["max"])
            # wealth is the number of periods worth of food owned by the agent
            # assumes that one good is instantly convertable to another
        
            self.wealth = sum(getattr(self, good) / self.model.consumption_rate[good]
                                     for good in self.model.goods)

        def setTargets():
            # set exchange target randomly at first
            goods = list(self.model.goods)
            random.shuffle(goods)
            self.target = goods.pop()
            self.not_target = goods[0]
               
        def mutate():
            # select which parameters will be mutated
            mutate_dict = {key: val if random.random() < self.mutate_rate else False for key, val in inheritance.items()} 
            # mutate select parameters
            selectParameters(mutate = True, **mutate_dict)
            
        if parent != None: inheritance = parent.defineInheritance()
        self.parent = parent
        self.model = model
        
        if self.parent:
            ####### parameters already inherited if agent has parent ########
            for attr, val in inheritance.items():
                setattr(self, attr, val)
            setStocks()
            # randomly set target, will be redifined in according to breed
            # parameters in the following period
            setTargets()
            # inherited values are mutated vals in dictionary if mutation is on
            if self.model.mutate:
                mutate()    
            else:
                self.selectBreedParameters(mutate = False,
                                           parent = self.parent,
                                           herding  = False)
        
        else:
            selectParameters()
        # allocate each .good to agent within quantity in range specified by 
        # randomly choose initial target good
        self.col = col
        self.row = row 
        self.dx = 0
        self.dy = 0
        self.id = ID
        self.reproduced = False

###############################################################################     
    def setBreedBasic(self, herder):
        self.basic = True
        self.switcher = False 
        self.arbitrageur = False
        self.herder = herder

    def selectBreedParameters(self, mutate, parent, herding = False, 
                              partner = None):
        def generateBreedParameters():
            if breed == "basic":
                self.target = "sugar"
                self.not_target = "water"
            # if breed == "switcher":
            #     switch_min = 5 if not mutate or"switch_rate"  not in inheritance else\
            #         int(inheritance["switch_rate"] / (1 + self.mutate_rate))
            #     switch_max = 50 if not mutate or "switch_rate" not in inheritance else\
            #         int(inheritance["switch_rate"] * (1 + self.mutate_rate))
            #     self.switch_rate = random.randint(switch_min, switch_max)
            #     self.periods_to_switch = self.switch_rate
                # start switcher with random target
 
            if breed == "arbitrageur":
                # track past exchange prices
                # if average prices is below price agent believes is correct,
                min_denominator = 10 if not mutate or "present_price_weight" not in inheritance else\
                    int(inheritance["present_price_weight"] / (1 + self.mutate_rate))
                max_denominator = 100 if not mutate  or "present_price_weight" not in inheritance else\
                    int(inheritance["present_price_weight"] * (1 + self.mutate_rate))
                self.present_price_weight = random.randint(
                    min_denominator, max_denominator)
                self.expected_price = self.reservation_demand["sugar"]["price"]

            if breed  == "herder":      
                self.wealthiest = parent if inheritance else self
                self.top_wealth = parent.wealth if inheritance else self.wealth
            # print("set attributes new:", breed)
        
        def copyPartnerParameters():
            # if copied breed and missing parameter value, draw from partner
            if getattr(self, breed):
                # if breed == "switcher":
                #     if not hasattr(self, 'switch_rate'):
                #         self.switch_rate = partner.switch_rate
                #     self.periods_to_switch = self.switch_rate
                #     self.basic = False
                if breed  == "herder":  
                    if not hasattr(self, "top_wealth"):
                        self.top_wealth = partner.wealth
                        self.wealthiest = partner
                if breed == "arbitrageur":
                    if not hasattr(self, "expected_price"):                        
                        self.expected_price = partner.expected_price
                    if not hasattr(self, "present_price_weight"):                    
                        self.present_price_weight = partner.present_price_weight 
                    # if not
                    # self.target = partner.target
                    # self.not_target = partner.not_target
          
        for breed in self.model.breeds:
            if getattr(self, breed):
                inheritance = parent.defineInheritance() if parent else ""
                # those who change breed due to herding need only need to fill missing
                # parameter values
                if herding:
                    copyPartnerParameters()
                else:
                    generateBreedParameters()        

    def defineInheritance(self):
        # use attributes to define inheritance
        copy_attributes = copy.copy(vars(self))
        # redefine "good" or else values are drawn from parent for children

        for key in self.model.drop_attr:
            try:
                del copy_attributes[key]
            except:
                continue 
        return copy_attributes
    
    def updateParams(self):
        def setTargetGood():
            self.wealth = sum((getattr(self,good) / self.model.consumption_rate[good] for good in self.model.goods))
            if self.herder:
                if self.wealth > self.top_wealth:
                    self.wealthiest = self
                if self.wealthiest != self:
                    self.top_wealth *= .999
            # let exchange target be determined by reservation demand
            # if shortage of both goods, choose randomly
            good1 = random.choice(self.model.goods)
            good2 = "water" if good1 == "sugar" else "sugar"
            # if self.basic and not self.arbitrageur:
            if self.switcher:
                if getattr(self,good1) < self.reservation_demand[good1]["quantity"]\
                    and getattr(self,good2) < self.reservation_demand[good2]["quantity"]:
                    self.target, self.not_target = good1, good2
                
                    # in case to level of wealth falls, as it does one population 
                    # grows, allow top_wealth to decay
                elif getattr(self,good1) < self.reservation_demand[good1]["quantity"]\
                    and getattr(self,good2) > self.reservation_demand[good2]["quantity"]:
                    self.target, self.not_target = good1, good2
                elif getattr(self,good2) < self.reservation_demand[good2]["quantity"]\
                    and getattr(self,good1) > self.reservation_demand[good1]["quantity"]:
                    self.target, self.not_target = good2, good1                
             
            if self.arbitrageur:
                # arbitrageur exchanges for the good that is cheaper than his WTP
                WTP = self.reservation_demand["sugar"]["price"]
                if self.expected_price > WTP:
                    self.target, self.not_target = "sugar", "water"  
                else: 
                    self.target, self.not_target = "water", "sugar"

        def checkReservation():
            for good in self.model.goods:
                if getattr(self, good) < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] *= self.price_change
                    self.reservation_demand[good]["quantity"] /= self.quantity_change
                if getattr(self, good) < self.reservation_demand[good]["quantity"]:
                    self.reservation_demand[good]["price"] /= self.price_change
                    self.reservation_demand[good]["quantity"] *= self.quantity_change
        # print(self.id)
        checkReservation()
        setTargetGood()




    def consume(self):
        for good, rate in self.model.consumption_rate.items():
            setattr(self,good, getattr(self,good) - rate)
            
            
    
    def checkAlive(self):
        for good in self.model.goods:
            if getattr(self, good) < 0:
                # self.model.dead_agent_dict[self.id] = self
                self.model.empty_patches[self.row, self.col] = self.model.patch_dict[self.row][self.col]
                if self.model.live_visual:
                    self.model.GUI.canvas.delete(self.image)
                del self.model.agent_dict[self.id]
                break
            
    def reproduce(self):
        if self.sugar > self.reproduction_criteria["sugar"] and\
            self.water > self.reproduction_criteria["water"]:
            # make sure inherited values are up to date

            self.model.total_agents_created += 1
            row, col = self.model.chooseRandomEmptyPatch()  
            ID = self.model.total_agents_created
            self.model.agent_dict[ID] =  Agent(self.model, row=row, col=col, 
                                               ID=ID, parent = self)
            self.model.agent_dict[ID].top_wealth = self.wealth
            self.model.agent_dict[ID].wealthiest = self
            self.model.patch_dict[row][col].agent =  self.model.agent_dict[ID]
            if self.model.live_visual:
                self.model.GUI.drawAgent(self.model.agent_dict[ID])
            self.reproduced = True


######################## move method and functions ############################
    def move(self):  
        
        def findMaxEmptyPatch(curr_row, curr_col):
            # dict to save empty patch with max q for each good
            max_patch = {good:{"Q":0,
                               "patch":None}
                         for good in self.model.goods}
            
            patch_moves = [(curr_row + dy, curr_col + dx)  
                           for dy in self.model.nav_dict[self.vision] if 0 <= curr_row + dy < 50
                           for dx in self.model.nav_dict[self.vision][dy] if 0 <= curr_col + dx < 50]
            
            # shuffle patches so not movement biased in one direction
            random.shuffle(patch_moves)
            near_empty_patch = False#{good: False for good in self.good}
            empty_patches = []
            for coords in patch_moves:   
                if coords in self.model.empty_patches.keys:
                    row, col = coords[0], coords[1]
                    empty_patch = self.model.patch_dict[row][col]
                    empty_patches.append(empty_patch)
                    patch_q = empty_patch.Q
                    patch_good = empty_patch.good
                    if patch_q > max_patch[patch_good]["Q"]:
                        # only mark near empty patch if Q > 0
                        near_empty_patch = True
                        max_patch[patch_good]["patch"] = empty_patch
                        max_patch[patch_good]["Q"] = patch_q
            return max_patch, near_empty_patch, empty_patches    

        def moveToMaxEmptyPatch(curr_row, curr_col, 
                                max_patch, near_empty_patch,
                                target, not_target, empty_patches):
            
            def basicMove(max_patch):
                max_q = max(max_patch[good]["Q"] for good in max_patch )
                # include both max water and max sugar patch if moth have max_q
                max_patches = [good for good in max_patch if max_patch[good]["Q"] == max_q]
                #randomly select max water or max sugar patch
                max_good = random.choice(max_patches) 
                target_patch = max_patch[max_good]["patch"]
                return target_patch
            
            def chooseTargetOrAlternate(max_patch, target, not_target, empty_patches):
                if type(max_patch[target]["patch"]) is Patch:
                    target_patch = max_patch[target]["patch"]
                    return target_patch
                # use elif with return within the if statement, that way
                # an error is thrown if target == not_target
                elif type(max_patch[not_target]["patch"]) is Patch:
                    # choose patch that moves agent closest to target 
                    # commodity
                    max_val = float("-inf")
                    min_val = float("inf")
                    for patch in empty_patches:
                        coord_sum = patch.col + patch.row 
                        if target == "sugar":
                            if coord_sum < min_val:
                                max_val = coord_sum
                                target_patch = patch
                        elif target == "water":
                            if coord_sum > max_val:
                                min_val = coord_sum
                                target_patch = patch
                                                
                    return target_patch
            
            ###################################################################  
            
    
            if near_empty_patch:
                if self.basic and not self.arbitrageur:
                    target_patch = basicMove(max_patch)
                else:
                    target_patch = chooseTargetOrAlternate(max_patch, target, not_target, empty_patches)
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
        max_patch, near_empty_patch, empty_patches = findMaxEmptyPatch(curr_row, curr_col)
        random.shuffle(empty_patches)
        
        # if near_empty_patch:
        moveToMaxEmptyPatch(curr_row, curr_col, max_patch, 
             near_empty_patch, self.target, self.not_target, empty_patches)


    
    def harvest(self):    
        agent_patch = self.model.patch_dict[self.row][self.col]
        setattr(self, agent_patch.good, getattr(self, agent_patch.good) + agent_patch.Q)
        agent_patch.Q = 0 

        
    def trade(self):
        
        def askToTrade(patch):
            partner = patch.agent
            #check if partner is looking for good agent is selling
            right_good = self.target != partner.target

            return partner, right_good

        def bargain(partner):       
            WTP = self.reservation_demand[self.target]["price"] 
            WTA = partner.reservation_demand[self.target]["price"]

            # assume bargaining leads to average price...
            # maybe change to random logged distribution later
            price, can_trade = (gmean((WTA, WTP)), True) if WTP > WTA else (None, False)
            return price, can_trade
        
        def executeTrade(partner, price):
                
            self_res_min = self.reservation_demand[self.not_target]["quantity"]
            partner_res_min = self.reservation_demand[self.target]["quantity"]
            while (getattr(self, self.not_target) > self_res_min > price) and\
                (getattr(partner, self.target) > partner_res_min > 1):
                
                setattr(self, self.target, getattr(self, self.target) + 1)
                setattr(self, self.not_target, getattr(self, self.not_target) - price)
                setattr(partner,self.target, getattr(partner, self.target) - 1)
                setattr(partner, self.not_target, getattr(partner, self.not_target) + price)
                
                # save price of sugar or implied price of sugar for every exchange
                transaction_price = price if self.target == "sugar" else 1 / price
                self.model.transaction_prices.append(transaction_price)
                self.model.total_exchanges += 1
                # record impact on arbitrageurs expected price of sugar
                if self.arbitrageur:
                    self.expected_price = (self.expected_price * (
                        self.present_price_weight) + transaction_price) / self.present_price_weight
        def herdTraits(agent, partner):
            def turn_off_other_primary_breeds(agent, breed, have_attr):
                if attr in self.model.primary_breeds:
                    # if breed changed, set other values false
                    if have_attr == True:
                        for brd in self.model.primary_breeds:
                            if brd != breed: 
                                setattr(agent, brd, False)
            # agent will copy partner traits. Sometimes, agent is self, 
            # sometimes not, so we call agent.selectBreedParameters at end
            if agent.herder:
                if agent.top_wealth < partner.wealth:
                    copy_attributes = partner.defineInheritance()
                    if agent.model.genetic:
                        for attr, val in copy_attributes.items():
                            if random.random() <= agent.model.cross_over_rate:
                                setattr(agent, attr, val)
                                # if attr is a primary breed, other breeds 
                                # will be switched off
                                turn_off_other_primary_breeds(agent, attr, val)
                        
                        # set basic True if all primary breeds switched to false
                        # due to genetic algorithm
                        if True not in (getattr(agent, breed)
                                        for breed in self.model.primary_breeds):
                            agent.setBreedBasic(herder = agent.herder)
                        agent.selectBreedParameters(mutate = False, parent = None, 
                                                   herding = True, partner = partner)
          
                    else: 
                        for attr, val in copy_attributes.items():
                            setattr(agent, attr, val)             

    ###############################################################################            

        # find trading partner
        neighbor_patches = [(self.row + i, self.col + j)
                        for i in self.model.nav_dict[1] if 0 <= self.row + i < 50
                        for j in self.model.nav_dict[1][i] if 0 <= self.col + j < 50 ]
        random.shuffle(neighbor_patches)
        for coords in neighbor_patches:
            if coords not in self.model.empty_patches.keys:
                row, col = coords[0], coords[1]
                target_patch = self.model.patch_dict[row][col]
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
                    if self.herder:
                        if self.top_wealth <  partner.wealth:
                            herdTraits(self, partner)
                    elif partner.herder:
                        if partner.top_wealth < self.wealth:    
                            herdTraits(partner, self)
                    
                    #  genetic?
                    # only trade with one partner per agent search
                    # agents can be selected by more than one partner
                    break
    


    
        
    


            
                
                
                
                
                
                
                
                
        