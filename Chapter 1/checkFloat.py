#checkFloat.py

import sys
print(sys.float_info)

x = 2.0 ** 1023
print(type(x))
print(x)

y = 2 ** 1025
print(type(y))
print(y)