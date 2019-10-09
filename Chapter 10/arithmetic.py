#arithmetic.py
from functools import reduce
from operator import mul

class Arithmetic():
    def __init__(self):
        self.target_value = 0
        
    def add(self, *args):
        try:
            self.target_value = sum([arg for arg in args])
            return self.target_value
        except:
            print("Pass int or float to add()")
    
    def multiply(self, *args):
        self.target_value = 1
        try:
            self.target_value = reduce(mul, args)
            return self.target_value
        except:
            print("Pass int or float to multiply()")
            
    def power(self, base, exponent):
        self.target_value = base ** exponent
        return self.target_value
    
arithmetic = Arithmetic()
print(arithmetic.target_value)
print(arithmetic.add(2,3,4))
print(arithmetic.multiply(2,3,4))
print(arithmetic.power(2,3))
