#minMaxFunctionsByHand.py

list1 = [20, 30, 40, 50]

### initial smallest value is very high
### will be replaced if a value from the list is lower
minListValue = 2 ** 1023

### initial largest value is very low
### will be replaced if a value from the list is higher
maxListValue = -2 ** 1023

for x in list1:
    if x < minListValue:
        minListValue = x
    if x > maxListValue:
        maxListValue = x

print("max:", maxListValue, "min:", minListValue)