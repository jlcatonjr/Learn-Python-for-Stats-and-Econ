#arithmetic.py
class Arithmetic():
    def __init__(self, initial_val):
        self.initial_val = initial_val
        pass
    
    def add(self, *args):
        try:
            total = 0
            for arg in args:
                total += arg
            return total
        except:
            print("Pass int or float to add()")
            
    def multiply(self, *args):
        product = 1
        try:
            for arg in args:
                product *= arg
            return product
        except:
            print("Pass only int or float to multiply()")
    
    def power(self, base, exponent):
        try:
            value = base ** exponent
            return value
        except:
            print("pass int or float for base and exponent")
            
arithmetic = Arithmetic(initial_val = 100)

print(arithmetic, "\n", arithmetic.__dict__)
print(arithmetic.add(1,2,3,4,5,6,7,8,9,10))
print(arithmetic.multiply(1,2,3,4,5,6,7,8,9,10))
print(arithmetic.power(4, 10))