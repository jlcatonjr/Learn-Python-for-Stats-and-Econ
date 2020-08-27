#integersAndFloats.py

x = 1
y = 1.
sumxy = x + y
print("x =", x)
print("y =", y)
print("x + y =", sumxy)
print("x is", type(x))
print("y is", type(y))
print("sumxy is", type(sumxy))

dct = {}
for i in range(0, 10.0):
    print(i)
    print(i + 1.)
    print(float(i))
    dct[str(i + 1.)] = i
    