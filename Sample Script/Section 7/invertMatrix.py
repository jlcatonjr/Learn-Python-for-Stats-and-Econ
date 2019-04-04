#invertMatrix.py
import numpy as np
#create vertical arrays
x1 = np.array([1,4,6])[:, None]
x2 = np.array([2,1,8])[:, None]
x3 = np.array([1,5,6])[:, None]

x1 = np.matrix(x1)
x2 = np.matrix(x2)
x3 = np.matrix(x3)

#join vectors into a 3x3 matrix
X = np.concatenate((x1, x2, x3), axis = 1)
invert_X = X.getI()
invert_X = np.round(invert_X, 2)

print("Array 1\n", x1)
print("Array 2\n", x2)
print("Array 3\n", x3)
print("Matrix of x1, x2, x3\n", X)
print("Inverted Matrix\n", invert_X)