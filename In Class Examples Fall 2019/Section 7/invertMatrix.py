#invertMatrix.py
import numpy as np
# create veritcal array
x1 = np.array([1, 2, 1])
x2 = np.array([4, 1, 5])
x3 = np.array([6, 8, 6])
print("Array 1:", x1, sep = "\n")
print("Array 2:", x2, sep = "\n")
print("Array 3:", x3, sep = "\n")
x1 = np.matrix(x1)
x2 = np.matrix(x2)
x3 = np.matrix(x3)
print("Row Vector 1:", x1, sep = "\n")
print("Row Vector 2:", x2, sep = "\n")
print("Row Vector 3:", x3, sep = "\n")
# axis = 0 stacks the row vectors
X = np.concatenate((x1, x2, x3), axis = 0)
X_inverse = np.round(X.getI(), 2)
X_transpose = X.getT()
print("X:", X, sep = "\n")
print("X Inverse:", X_inverse, sep = "\n")
print("X Transpose:", X_transpose, sep = "\n")