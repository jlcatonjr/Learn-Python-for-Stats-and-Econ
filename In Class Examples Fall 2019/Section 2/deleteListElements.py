#deleteListElements.py

# create two lists with elements that strings
list1 = ["red", "blue", "orange", "black", "white", "golden"]
list2 = ["nose", "ice", "fire", "cat", "mouse", "dog"]
len_list1 = len(list1)
len_list2 = len(list2)

#check that the length of list1 equals the length of list2
if len_list1 == len_list2:
    #if condition is met, print ith elements from each list, separated by a tab
    for i in range(len_list2):
        print(list1[i].upper(), "\t", list2[i].title())

# delete an element from each list
del list1[0]
del list2[5]

len_list1 = len(list1)
len_list2 = len(list2)

print()
print("lists after deletion:")
if len_list1 == len_list2:
    for i in range(len_list1):
        print(list1[i], "\t", list2[i])

# use slice
print("Every other elemnt:", list1[::2])

for i in range(len_list1):
    for j in range(len(list1[i])):
        print(list1[i][j])

print()
word = "supercalfragalisticexpialidocious"
for letter in word:
    print(letter)