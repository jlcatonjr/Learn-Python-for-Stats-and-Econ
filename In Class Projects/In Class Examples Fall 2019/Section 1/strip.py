#stripAlternate1.py
spaces = "    Look at all the spaces in the text!    "
print("no spaces removed:\n", spaces)

remove_left_spaces = spaces.lstrip()
remove_right_spaces = spaces.rstrip()
remove_left_and_right_spaces = spaces.strip()

print("Remove left spaces:", remove_left_spaces,
      "Remove right spaces:",remove_right_spaces, 
      "Remove left and right spaces:", remove_left_and_right_spaces, sep="\n")