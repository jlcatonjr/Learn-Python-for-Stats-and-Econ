primes = []
for i in range(2, 100000):
    if len(primes) > 1000:
        break
    for j in range(2, i):
        if i % j == 0 and i != 2:
            break
        if j == i - 1:
            primes.append(i)

print(primes)
# this generator checks every number from 2 to 100 to see if it is prime
# to do so it creates a list of True and False elements, where True is returned
# when i % j == 0. If a true is returned, than this means that j is divisible 
# by a number other than 1 and itself. Thus, it fails to meet the condition of 
# being prime, which is identified by the filter: 
# if True not in list-created-by-generator
# If this is the case, the number i is not recorded and the next i is checked
# for being prime or not
primes = [i for i in range(2,100) if True not in [i % j == 0 for j in range(2,i)]] 