#countEvenNumbersForLoop.py

evenNumbers = []
countByThrees = []
for i in range(1001):
    if i % 2 == 0:
        evenNumbers.append(i)
    if i % 3 == 0:
        countByThrees.append(i)

print(evenNumbers)
print(countByThrees)