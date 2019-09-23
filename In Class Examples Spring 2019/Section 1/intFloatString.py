#intFloatString.py
x = 11
y = "11"
print("x =", x)
print("y =", y)
print('x\'s type:', type(x))
print("y's type:", type(y))

try:
    print(x + y)
except:
    print("Error: cannot add together", type(x), "and", type(y))
    
print("Concatenate strings:",str(x) + y)
print("Add integers:", x + int(y))