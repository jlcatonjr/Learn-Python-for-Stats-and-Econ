lst = [1,2,3,4,5,6,7]
sliced_lst = lst[2:5]
# unspecified slice values default:
#   lst[:] == lst[0:len(lst)]
full_slice_list = lst[:]
beginning_slice = lst[:4]
end_slice = lst[3:]

random_list = [23,652,5473,32532,44,3]
sliced_random_list = random_list[2:5]


print("lst[2:5]:\n",sliced_lst)
print("random_list[2:5]:\n", sliced_random_list)
print("lst[:]:\n", full_slice_list)
print("lst[:4]:\n", beginning_slice)
print("lst[3:]\n", end_slice)