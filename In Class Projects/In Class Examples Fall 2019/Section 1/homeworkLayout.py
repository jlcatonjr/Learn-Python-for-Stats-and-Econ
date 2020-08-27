import numpy as np
import decimal
import string
#homeworkLayout.py
print("""
James Caton
ECON 411 / 611
Homework
""")

print("""
1. Record your name in an object (x = ...) and a description of yourself in 
another object. 
""")

#first name
first = "James"
#middle name
middle = "Lee"
#last name
last = "Caton"
#full name combines the first middle and last
full_name = first + " " + middle + " " + last

print("""
SCRIPT:
#first name
first = "James"
#middle name
middle = "Lee"
#last name
last = "Caton"
#full name combines the first middle and last
full_name = first + middle + last

RESULT:
""")
print(full_name)

print("""
EXPLANATION:
I save my first middle and last names as three separate string objects and then 
concatenate them in one object name full_name.
""")


    
    

print("""
2. Raise 2 to the 4th power. Save the value as an object named 
two_to_the_fourth. Then create a new value that sums the value twice. 
Create another variable that saves the value of twoToTheFourth as a string. 
Just as with the numeric value, sum the string object twice.
""")

two_to_the_fourth = 2 ** 4
two_to_the_fourth_summed_twice = two_to_the_fourth + two_to_the_fourth
two_to_the_fourth_string = str(two_to_the_fourth)
two_to_the_fourth_summed_twice_string = two_to_the_fourth_string + two_to_the_fourth_string 
print("""
SCRIPT:

two_to_the_fourth = 2 ** 4
two_to_the_fourth_summed_twice = two_to_the_fourth + two_to_the_fourth
two_to_the_fourth_string = str(two_to_the_fourth)
two_to_the_fourth_summed_twice_string = two_to_the_fourth_string + two_to_the_fourth_string 
    
    
RESULT:
""")

print(two_to_the_fourth)
print(two_to_the_fourth_summed_twice)
print(two_to_the_fourth_string)
print(two_to_the_fourth_summed_twice_string )

print("""
Explanation:
The value  2 ** 4 was saved as two_to_the_fourth. By summing the value twice,
we produced 32. When two_to_the_fourth was saved as a string, using the +
sone resulted in the string version of the value being concatenated, thus
producing 1616.
""")    
    
    
    
    
print("""
3. Find the list of escape sequences in section 2.4: 
https://docs.python.org/3/reference/lexical_analysis.html#literals 
create a string that uses at least 4 different escape sequences.
""")

tab_word = "I use the \t tab escape sequence"
new_line = "It was boring,\nso I made a new line"
escape_quote = "How \"convenient\" it is to include scare quote"
backslash = "And who knew that \"\\\" did so much work!"

    
print("""
SCRIPT:
tab_word = "I use the \\t tab escape sequence"
new_line = "It was boring,\\nso I made a new line"
escape_quote = "How \\"convenient\\" it is to include scare quote"
backslash = "And who knew that \\"\\\\\\" did so much work!"

    
RESULT:
""")  
print(tab_word, new_line, escape_quote, backslash, sep="n")
    
    







print("""    
4. Add an integer and a float together. Is the final number an integer or a 
float?
""")


print("""
SCRIPT:

    
    
RESULT:
""")


    
    
    
    
    
    
    
print("""
5. Add 2 ** 1024 + 1.5. What is the outcome? Why? hint: Try adding .5, 1, and  
1.1 instead of 1.5.
""")
val = 2 ** 1024
# 2 ** 1024 + 1.0 is to large of a value to fit in the float datatype
#new_val0 = 2**1024 + 1.0 
#similar error as above
new_val1 = decimal.Decimal(val) + decimal.Decimal(.5)
new_val2 = val + 1
#same float error
#new_val3 = val + 1.1

print("""
SCRIPT:

    
    
RESULT:
""")
print(val)
print(new_val1)
print("""
EXPLANATION: Python has constraints in regard to the size of values saved as
floats (values decimals). 2.0**1024 is too large to be contained as a float.
When you add a float to an integer, the result is converted into a float. Thus
2 ** 1024 + 1.0 results in a value that cannot be contained as a float...""")

print("""
6. import the string library with the script "import string". Print 
string.__dict__ . What is the output? If you do not understand the meaning,
search "python class __dict__" and find an explanation.
""")
print(string.__dict__)
