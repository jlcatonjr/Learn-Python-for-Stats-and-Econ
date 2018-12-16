#zerosOnesAndLike.py

listOfLists = [[1,2,3],[4,5,6],[7,8,9]]
arrayOfArrays = np.array(listOfLists)
zerosLikeArray = np.zeros_like(listOfLists)
onesLikeArray = np.ones_like(listOfLists)
emptyLikeArray = np.empty_like(listOfLists)

print("listOfLists:\n", listOfLists)
print("arrayOfArrays:\n", arrayOfArrays)
print("zerosLikeArray:\n", zerosLikeArray)
print("onesLikeArray:\n", onesLikeArray)
print("emptyLikeArray:\n", emptyLikeArray)