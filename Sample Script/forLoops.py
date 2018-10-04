#forLoops.py
# import pandas data structures library
import pandas as pd


start = 1
end = 100
isPrime = {}

# Number we are checking if prime
for i in range(start, end + 1):
    # 1, 2, and 3 are all prime
    if i < 4:
        print(str(i) + " is a prime number")
        isPrime[i] = [True]
        # "continue" will stop processing script for
        # the current iteration within a for-loop
        # nothin executed below "continue"
        continue
    
    #check every number between 2 and i - 1
    for j in range(2,i): 
        #that there is a remainder 
        remainder = i % j

#       if there is no remainder, then the number is not prime        
        if remainder == 0:
            print(str(i) + " is not a prime number")
            isPrime[i] = [False]

            #go back to previous for loop
            #break out of for loop
            break
        # if j has reached i - 1 w/out creating remainder of 0
        # then i is prime
        if j == i - 1:                
            print(str(i) + " is a prime number")
            isPrime[i] = [True]

for i in range(start, end + 1):
    print("Is " + str(i) + " prime?\n" + str(isPrime[i]))
    
# Use pandas to turn dictionary into dataframe
isPrimeDF = pd.DataFrame(isPrime)

#creates a new column
isPrimeDF[" "] = "Is Number Prime?"

# select new column as index
isPrimeDF = isPrimeDF.set_index(" ")
isPrimeDF = isPrimeDF.T
print(isPrimeDF)
isPrimeDF.to_csv("isPrime1To100.csv")
