#RPG.py
import agent
import random
import sys
import time
import copy

class RPG():    
    difficultyAdjustDict = {"easy":.8, "normal":1, "difficult":1.2}
    
    def __init__(self, num_humans, num_computers, difficulty):
        self.num_humans= num_humans
        self.num_computers = num_computers
        self.difficulty = difficulty.lower()
        self.agent_dict = {}
        self.human_ids = []
        self.computer_ids = []
        self.create_players()
        
    def create_players(self,):
        for h in range(self.num_humans):
            self.agent_dict[h] = agent.Agent( rpg = self, hp = 20, mp = 10, strength = 5, defense = 5, magic = 5, id_num = h, computer = False, difficulty = self.difficulty)
            self.human_ids.append(h)
        lowest_computer_id = h + 1
        for c in range(lowest_computer_id, lowest_computer_id +  self.num_computers):
            self.agent_dict[c] = agent.Agent(rpg = self, hp = 20, mp = 10, strength = 5, defense = 5, magic = 5, id_num = c, computer = True, difficulty = self.difficulty)
            self.computer_ids.append(c)

    def play_tournament(self):
        #create simpler reference for human and computer dicts
        alive_players_dict = self.identify_live_agents(self.agent_dict)
        
        #If a human is alive, continue Tournament
        while True in [self.agent_dict[key].alive for key in self.agent_dict]:
            
            rand_order_id_list = list(alive_players_dict.keys())
            random.shuffle(rand_order_id_list)
            
            while len(rand_order_id_list) > 1:
                id_player_1 = rand_order_id_list.pop()
                id_player_2 = rand_order_id_list.pop()
                print("Battle between player", id_player_1, "and player", id_player_2)
                self.battle(id_player_1,id_player_2)
            alive_players_dict = self.identify_live_agents(self.agent_dict)
            if len(rand_order_id_list) == 1:
                id_player1 = rand_order_id_list.pop()
                if len(alive_players_dict.keys()) == 1:
                    print("Player", id_player1, "won the tournament!!!")
                    sys.exit()
                else:
                    print("Lucky player", id_player1, "moves to the next round!")
            
    def identify_live_agents(self, agent_dict):
        alive_dict = {}
        for key in agent_dict:
            agent = agent_dict[key]
            if agent.alive:
                alive_dict[key] = agent_dict[key]
        return alive_dict
    
    def battle(self, id_player_1, id_player_2):
        player_1 = self.agent_dict[id_player_1]
        player_2 = self.agent_dict[id_player_2]
        while (player_1.alive ==True and player_2.alive == True):
            player_1.choose_move(player_2)
            player_2.choose_move(player_1)
        
        # Heal winner for next round of fighting
        if player_1.alive: 
            print("Player", player_1.id_num, "won!")
            player_1.record["Wins"] +=1
            player_2.record["Losses"] +=1
            player_1.hp = copy.copy(player_1.max_hp)
        if player_2.alive:
            print("Player", player_2.id_num, "won!")
            player_2.hp = copy.deepcopy(player_2.max_hp)
            player_2.record["Wins"] += 1
            player_1.record["Losses"] += 1
        time.sleep(3)
                
