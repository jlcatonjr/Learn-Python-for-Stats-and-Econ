#primeNumbers.py
import time

start2 = time.time()
primes1 = [i for i in range(2,10000) if True not in [i % j == 0 for j in range(2,int(i) if i % 2 == 0 else int(i / 2))]]
end2 = time.time()
time2 = end2 - start2
print(time2)


start = time.time()
primes2 = [i for i in range(2,10000) if True not in [i % j == 0 for j in range(2,int(i / 2 + 1) if i % 2 == 0 else int(i / 2))]]
end = time.time()
time1 = end - start 
print(time1)