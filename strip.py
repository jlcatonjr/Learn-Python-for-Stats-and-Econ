#strip.py
spaces = "    Look at all the spaces in the text!    "
print("no spaces removed:\n", spaces)

removeLeftSpaces = spaces.lstrip()
removeRightSpaces = spaces.rstrip()
removeLeftAndRightSpaces = spaces.strip()

print("Remove left spaces:\n" + removeLeftSpaces)
print("Remove right spaces:\n" + removeRightSpaces)
print("Remove left and right spaces:\n" + removeLeftAndRightSpaces)

