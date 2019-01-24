#createMinMaxFunction.py

def minimum_value(lst):
    #check if any ints or floats are in the list
    type_list = check_list_types(lst)
    #if not, return error
    if float not in type_list and int not in type_list:
        return "error"
    # if not create check every value in list against the value assigned to minimum
    # default value for minimum is inf
    minimum = float('inf')
    for val in lst:
        try:
            if val < minimum:
                minimum = val
        except:
            return_operator_error(val)
    return minimum

def maximum_value(lst):
    #check if any ints or floats are in the list
    type_list = check_list_types(lst)
    #if not, return error
    if float not in type_list and int not in type_list:
        return "error"
    # if not create check every value in list against the value assigned to minimum
    # default value for minimum is inf
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
    # create a list called type_list that records type every element in lst
    type_list = [type(val) for val in lst]
    #reduce this list with set() to record each type only once
    #convert set() to list()
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

print("Minimum value from list1:", min_list1)
print("Maximum value from list1:", max_list1)
print("Minimum value from string_list:", min_string)
print("Maximum value from string_list:", max_string)
print("Minimum value from mixed_list:", min_mixed)
print("Maximum value from mixed_list:", max_mixed)