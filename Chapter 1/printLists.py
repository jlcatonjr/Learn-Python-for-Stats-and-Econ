#printLists.py
num1 = 5 / 3
num2 = 5 / 4
num3 = 4 / 3
numList = [num1, num2, num3]
numLabel = ["num1:", "num2:", "num3:"]
print("num1:", num1, "\nnum2:", num2, "\nnum3:", num3)
print(numLabel, numList)

print("\nOr we can print the ith element for each list for all j elements")
j = len(numList)
for i in range(j):
    print(numLabel[i],numList[i])
