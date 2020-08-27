#printLists.py
num1 = 5 / 3
num2 = 5 / 4
num3 = 4 / 3
print("num1:", num1, "\nnum2:", num2, "\nnum3:", num3)
print(num_label, num_list)

print("\nOr we can print the ith element for each list for all j elements")
num_list = [num1, num2, num3]
num_label = ["num1:", "num2:", "num3:"]
# len() provides the length of the list passed to it
# that value is used to call each index using the for-loop
j = len(num_list)
for i in range(j):
    print(num_label[i],num_list[i])
