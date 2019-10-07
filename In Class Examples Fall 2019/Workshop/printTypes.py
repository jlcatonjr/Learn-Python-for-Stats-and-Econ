import random
class Fish():
    
    def __init__(self, name, color, gender, species, weight):
        self.name = name
        self.color = color
        self.gender = gender
        self.species = species
        self.weight = weight
        self.age = 0
        self.stamina = "low" if random.randint(0,1) == 0 else "high"
        self.speed = "slow" if random.randint(0,1) == 0 else "fast"
        print("A fish is born")
        print("This fish's name is", name + ".", name, "is a", weight, ",", color, ",", 
              gender, species)
    
    def swim(self, distance):
        #slow fish travel at 1 meter per second
        #fast fish travel at 2 meters per second
        if self.speed == "slow":
            rate_of_movement = 1
        else:
            rate_of_movement = 2
            
        if self.stamina == "low":
            rate_of_movement_after_fifty_meters = rate_of_movement / 2
        else:
            rate_of_movement_after_fifty_meters = rate_of_movement
        
        seconds_travelled = distance / rate_of_movement
        print("The fish travelled", distance, "meters in", seconds_travelled,
              "seconds")
        
        return seconds_travelled
        # if a fish with low stamina travels over 50 meters, it's speed is 
        # halved
        
        # high stamina fish never get tired...
        
        
        #identify the average speed of the fish over some distance and the time
        # taken to complete the swim
        
        
fish = Fish(name = "Harold", color = "blue and gold", gender = "male", 
            species = "shubunkin", weight = "4 ounces")

distance_dict = {}
for i in range(101):
    distance_dict[i] = fish.swim(i)

print(distance_dict)
#print(fish)
#
#x = " D F"
#y = 1
#
#print("x is a:", type(x))
#print("y is a:", type(y))
#
#lst = [i for i in range(20)]
#type_lst = [type(val) for val in lst]
#print(type_lst)
#print(type([[],[],[]]))
#
#
#
##
##for val in lst:
##    val_type = type(val)
##    print(val_type)
##    