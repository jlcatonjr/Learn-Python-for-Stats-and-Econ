#arithmetic.py
class Arithmetic():

    def __init__(self,  ):
        pass
    
    def add(self, *args):
        try:
            total = sum([arg for arg in args])
            return total
        except:
            print("Pass only int or float to add()")
            
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
            print("Pass int or float for base and exponent")
            
arithmetic = Arithmetic()
print(arithmetic)
print(arithmetic.add(1,2,3,4,5,6,7,8,9,10))
print(arithmetic.multiply(2,3,4))
print(arithmetic.power(2,3))