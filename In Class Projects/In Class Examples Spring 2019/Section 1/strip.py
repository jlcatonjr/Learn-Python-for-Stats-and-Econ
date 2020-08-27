#strip.py

spaces = "    Look at all the spaces in the text!    "
print("no spaces removed:\n", spaces)

remove_left_spaces = spaces.lstrip()
remove_right_spaces = spaces.rstrip()
remove_left_and_right_spaces = spaces.strip()
remove_all_spaces = spaces.replace(" ", "")
replace_space_with_underscore = spaces.replace(" ","_")
replace_space_with_underscore_2 = remove_left_and_right_spaces.replace(" ", "_")

print("Remove left spaces:\n" + remove_left_spaces)
print("Remove right spaces:\n" + remove_right_spaces)
print("Remove left and right spaces:\n" + remove_left_and_right_spaces)
print("Remove all spaces:\n"+ remove_all_spaces)
print("Replace spaces with underscore:\n" + replace_space_with_underscore )
print("Replace spaces with underscore:\n" + replace_space_with_underscore_2)