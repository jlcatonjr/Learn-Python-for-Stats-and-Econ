#baseCounting.py
#imagine that you wanted to count to base ** 3 - 1
count_list = []
base10_count_list = []
# try changing the base to see how the count changes
# the program will count to base ** 3 - 1
# provides interpretable results work for all bases up to 10
base = 2
base_10_val = 50
dig_place = 0

while base_10_val / base > 1:
    dig_place += 1
    base_10_val /= base

print(dig_place)

#for i in range(base):
#    for j in range(base):
#        for k in range(base):        
#            val = int(str(i) + str(j) + str(k))
#            count_list.append(val)
#            #produce equivalent list in base10
#            base10_val = i * base ** 2 + j * base + k
#            base10_count_list.append(base10_val)
#
#print("\ncount in base", base)
#print(count_list)
#print("\ncount in base 10:")
#print(base10_count_list)