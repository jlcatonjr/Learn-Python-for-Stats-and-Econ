#lineAndRandomPoints.py
import numpy as np
import matplotlib.pyplot as plt
import random

line = np.array([i + 3 for i in range(100)])
figure = plt.figure(figsize = (12,6))
points = []
for point in line:
    points.append(random.normalvariate(point, point))
plt.plot(line)
plt.scatter(np.arange(len(points)), points, s = 10)
plt.text(len(line) * 1 / 4, line[int(len(line)*1/4)] + 80, "Truth", fontsize = 20)
plt.arrow(len(line) * 1 / 4 + 4, line[int(len(line)*1/4) - 5] + 80, 10, -50, 
          linewidth = 3,head_width = 5,head_length = 8)
print(line)
plt.show()