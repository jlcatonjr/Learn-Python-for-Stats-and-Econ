import random
import pandas as pd
random_dict = {}

for i in range(10):
    random_dict[i] = [int(random.random() * 1000) for j in range(100)]

random_df = pd.DataFrame(random_dict)
print(random_df)
