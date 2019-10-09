#agent.py
import random
class Agent():
    
    def __init__(self, rpg, hp, mp, strength, defense, magic, id_num, difficulty, computer = True):
        self.rpg = rpg
        self.id_num = id_num
        self.alive = True
        self.record = {"Wins": 0, "Losses": 0}

        if computer == False:
            self.strength = strength
            self.hp = hp
            self.max_hp = hp
            self.mp = mp
            self.max_mp = mp
            self.defense = defense
            self.magic = magic
            self.type = "human"
        if computer:
            adjustment = self.rpg.difficultyAdjustDict[difficulty]
            self.strength = random.randint(int(.5 * strength), int(strength * adjustment))
            self.hp = random.randint(int(.5 * hp), int(hp * adjustment))
            self.max_hp = hp
            self.mp = random.randint(int(.5 * mp), int(mp * adjustment))
            self.max_mp = mp
            self.defense = random.randint(int(.5 * defense), int(defense * adjustment))
            self.magic = random.randint(int(.5 * magic), int(magic * adjustment))
            self.type = "computer"
            
            
            
    def choose_move(self, defender):
        next_player = False
        if defender.alive == False or self.alive == False: next_player = True
        while (next_player == False):
            if self.type == "human":
                move = input("Choose your move player " + str(self.id_num) + "\n1: Attack\n2: Recover")
            if self.type == "computer":
                move = str(random.randint(1,2))
            if move == "1":
                self.attack(defender)
                next_player = True
            else:
                if move == "2":
                    self.recover()
                else:
                    print("Enter either '1' or '2'")
                    
    def attack(self, defender):
        hp_loss = self.strength - (defender.defense ** .5)
        if hp_loss < 0: hp_loss = 0
        defender.hp += -hp_loss
        defender.check_health()
        print("Player", defender.id_num, "lost", hp_loss, "HP!" )
        print("HP:", defender.hp)
        print("MP:", defender.mp)
        
    def recover(self):
        if self.mp > 0:
            self.hp += self.magic
            if self.hp > self.max_hp: self.hp = self.max_hp
            self.mp += -1
            print("Player", self.id_num, "recovered HP!")
            print("HP:", self.hp)
            print("MP:", self.mp)
            next_player = True
        else:
            print("Not enough MP to recover!")
                
    def check_health(self):
        if self.hp <= 0: 
            self.hp = 0
            self.alive = False
        if self.alive:
            print("Player", self.id_num, "is alive")
        else:
            print("Player", self.id_num, "is dead")