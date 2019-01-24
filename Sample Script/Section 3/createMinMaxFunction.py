#createMinMaxFunction.py

def minimum_value(lst):
    type_list = check_list_types(lst)
    if float not in type_list and int not in type_list:
        return "error"
    minimum = float('inf')
    for val in lst:
        try:
            if val < minimum:
                minimum = val
        except:
            return_operator_error(val)
    return minimum

def maximum_value(lst):
    type_list = check_list_types(lst)
    if float not in type_list and int not in type_list:
        return "error"
    maximum = float('-inf')
    for val in lst:
        try:
            if val > maximum:
                maximum = val
        except:
            return_operator_error(val)
            
    return maximum

def return_operator_error(val):
    print("object is type:", type(val), "Cannot apply operator")
    
def check_list_types(lst):
    type_list = [type(val) for val in lst]
    types = list(set(type_list))
    return types

list1 = [12,24,33,485]
string_list = ["These", "are", "strings", "not", "values"]
mixed_list = [1,2,35,"fdsajfsa",3128473217980]

min_list1 = minimum_value(list1)
max_list1 = maximum_value(list1)
min_string = minimum_value(string_list)
max_string = maximum_value(string_list)
min_mixed = minimum_value(mixed_list)
max_mixed = maximum_value(mixed_list)
print(min_list1)
print(max_list1)
print(min_string)
print(max_string)
print(min_mixed)
print(max_mixed)