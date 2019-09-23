import copy

print("""
James Caton
ECON 611
Homework 2
""")

print("""
1. Create a list of numbers at least 100 elements in length that counts by 3s -
 i.e., [3,6,9,12,...]
""")

# use generator to create a list that counts by 3s by mulitplying each
# i by 3
lst = [i * 3 for i in range(0,330)]

print("""
SCRIPT:
# use generator to create a list that counts by 3s by mulitplying each
# i by 3
lst = [i * 3 for i in range(0,330)]

RESULT:
""")
print(lst)

print("""
EXPLANATION:
I could have passed 3 to the last range function - i.e., range(0, 990, 3)
but I accomplished the same outcome by multiplying each i by 3 instead.
""")


print("""
2. Using the list from question 1, create a second list whose elements are the 
same values converted to strings. hint: use str().
""")

# use a generator to call each value from lst and transform to string
string_lst = [str(val) for val in lst]

print("""
SCRIPT:
# use a generator to call each value from lst and transform to string
string_lst = [str(val) for val in lst] 
RESULT:
""")
print(string_lst)

print("""
EXPLANATION:
I used a generator to create a list where I called each value from lst, 
and transformed the value into a string. Since generator calls all of the 
values from lst, this create a list that is identical to lst except that
the elements are strings, not integers.
""")

print("""
3. Using the list from question 2, create a variable that concatenates each of 
the elements in order of index (Hint: result should be like "36912...").
""")


print("""
EXPLANATION:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    
print("""
4. Using .pop() and .append(), create a list whose values are the same as the 
list from question 1 but in reverse order.
""")

#lst2 = copy.copy(lst)
#lst_copy = []
#for val in lst:
#    lst_copy.append(val) 
lst_copy = lst[:]

new_lst = []
for i in range(len(lst)):
    j = len(lst) - 1
    x = lst[j]
    new_lst.append(x)
    del lst[j]

    
    
    
    
    
#    x = lst_copy.pop()
#    new_lst.append(x)

print(new_lst)    


print("""
EXPLANATION:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    

print("""
5. Using a slice and len(), create a list that includes only the second half of
 the list from question 1.
""")


print("""
SCRIPT:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    
print("""
6 Create a string that includes only every other element, starting from the 0th 
element, from the string in question 3 while maintaining the order of these 
elements (Hint: this can be done be using a for loop whose values are descending).
""")


print("""
SCRIPT:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    
print("""
7. Explain the difference between a dynamic list in Python (usually referred to 
as a list) and an array.
""")


print("""
SCRIPT:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    
print("""
Exploration:
1. Use a generator to create a list of the first 1000 prime numbers. Include a 
paragraph explaining how a generator works.
""")


print("""
SCRIPT:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    
print("""
2. Using a for loop and the pop function, create a list of the values from the 
list of prime numbers whose values are descending from highest to lowest.
""")


print("""
SCRIPT:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    
print("""
3. Using either of prime numbers, create another list that includes the same 
numbers but is randomly ordered. Do this without shuffling the initial list 
(Hint: you will need to import random and import copy). Explain in a paragraph 
the process that you followed to accomplish the task.
""")


print("""
SCRIPT:
    
RESULT:
""")

print("""
EXPLANATION:
""")
    
    