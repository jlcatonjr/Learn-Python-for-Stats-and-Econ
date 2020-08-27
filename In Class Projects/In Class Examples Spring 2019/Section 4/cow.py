import random

class Cow():
    def __init__(self, name, gender, favorite_food):
        self.name = name
        self.gender = gender
        self.favorite_food = favorite_food
        self.weight = random.randint(800,1200)
    
    def moo(self):
        print("%s loooveess too mooooo." % self.name)
    
    def eat(self):
        self.weight += 1
        print("Yuuummmmmm. %s just ate her favorite food: %s"\
              % (self.name, self.favorite_food))
        print("%s weighs %i pounds!" % (self.name, self.weight))
    
    def poop(self):
        self.weight -=1
        print("%s feels relieved!" % self.name)
        print("%s weighs %i pounds!" % (self.name, self.weight))
    def talk_to_cow_friend(self, cow_friend):
        print("%s told her friend %s about her favorite food: %s!!"\
               % (self.name, cow_friend.name, self.favorite_food))
        print("%s doesn't understand how any cow could like anything but %s!"\
               % (cow_friend.name, cow_friend.favorite_food))
        
bessie = Cow( gender = "Lady Cow", name = "Bessie", favorite_food = "dry grass")
moooe = Cow("Moooe", "Brown Cow Bro", "wet grass")

bessie.eat()
bessie.moo()
bessie.poop()
bessie.talk_to_cow_friend(moooe)