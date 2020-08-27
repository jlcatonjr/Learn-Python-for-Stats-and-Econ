#homework1Help.py
print("""
James Caton
ECON 411
Homework 1""")

print("""
1. Record your name in an object (x = ...) and a description of yourself in 
another object.
""")

name = "Jim"
bio = """I am an economist who teaches at NDSU. I teach economic computation, 
macroeconomics, institutions, entrepreneurship."""

print("""
SCRIPT:
    
name = "Jim"
bio = \"""I am an economist who teaches at NDSU. I teach economic computation, 
macroeconomics, institutions, entrepreneurship.\"""

RESULT: 
""")
print(name)
print(bio)

print("""
2. Raise 2 to the 4th power. Save the value as an object named twoToTheFourth. 
Then create a new value that sums the value twice. Create another variable that 
saves the value of twoToTheFourth as a string. Just as with the numeric value, 
sum the string object twice.
""")

# Create two to the fourth power using **
two_to_the_fourth = 2 ** 4
# use two_to_the_fourth to make a value twice as large
two_to_the_fourth_summed_twice = two_to_the_fourth + two_to_the_fourth
two_to_the_fourth_string = str(2 ** 4)
two_to_the_fourth_string_summed_twice = two_to_the_fourth_string + two_to_the_fourth_string


print("""
SCRIPT:
# Create two to the fourth power using **
two_to_the_fourth = 2 ** 4
# use two_to_the_fourth to make a value twice as large
two_to_the_fourth_summed_twice = two_to_the_fourth + two_to_the_fourth
two_to_the_fourth_string = str(2 ** 4)
two_to_the_fourth_string_summed_twice = two_to_the_fourth_string + two_to_the_fourth_string

RESULTS:
""")

print(two_to_the_fourth)
print(two_to_the_fourth_summed_twice)
print(two_to_the_fourth_string)
print(two_to_the_fourth_string_summed_twice)
#print("""
#3. Find the list of escape sequences in section 2.4: 
#https://docs.python.org/3/reference/lexical_analysis.html#literals 
#create a string that uses at least 4 different escape sequences.
#""")
#    
#print("""
#4. Add an integer and a float together. Is the final number an integer or a 
#float?
#""")
#
#
#print("""
#5. Add 2 ** 1024 + 1.5. What is the outcome? Why? hint: Try adding .5, 1, and  
#1.1 instead of 1.5.
#""")
