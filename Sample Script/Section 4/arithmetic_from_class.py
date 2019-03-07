class Arithmetic():
    def __init__(self):
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
        print(args)
        product = 1
     
        try:
            for arg in args:
                product *= arg
            return product
        
        except:
            print("Pass pass only int or float to multiply()")
            
arithmetic = Arithmetic()
print(arithmetic)
print(arithmetic.add(1,2,5,6,7,3,6,5,78,43,6,7,45))
print(arithmetic.multiply(1,2,3,5,756,52,23))