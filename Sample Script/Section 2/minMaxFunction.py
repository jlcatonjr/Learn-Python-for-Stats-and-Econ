#minMaxFunction.py
import sys

list1 = [20, 30, 40, 50]
max_list_value = max(list1)
min_list_value = min(list1)
print("maximum:", max_list_value, "\nminimum:", min_list_value)

minimum = 99999
maximum = -99999
for val in list1:
    if val < minimum:
        minimum = val
    if val > maximum:
        maximum = val
print("maximum:", maximum, "\nminimum:", minimum)