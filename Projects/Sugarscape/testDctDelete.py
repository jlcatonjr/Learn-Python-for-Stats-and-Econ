#test.py
import time

def time_del(dct, key):
    start = time.time()
    del dct[key]
    end = time.time()
    elapse = end - start
    return elapse
dct1 = {i:{j:str(i*j)} for i in range(1000) for j in range(1000)}
dct2 = {i:{j:str(i*j)} for i in range(10000) for j in range(1000)}

print(time_del(dct1,100))
print(time_del(dct2, 100))
