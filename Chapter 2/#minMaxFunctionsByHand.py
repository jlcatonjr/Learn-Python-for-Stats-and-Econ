#minMaxFunctionsByHand.py

list1 = [20, 30, 40, 50]

### initial smallest value is very high
### will be replaced if a value from the list is lower
min_list_value = 2 ** 1023

### initial largest value is very low
### will be replaced if a value from the list is higher
max_list_value = -2 ** 1023

for x in list1:
    if x < min_list_value :
        min_list_value = x
    if x > max_list_value :
        max_list_value = x

print("maximum:", max_list_value , "minimum:", min_list_value )