import numpy as np
import matplotlib.pyplot as plt
import random
#lineAndRandomPoints.py
line = np.array([i + 3 for i in range(100)])
points = []
for point in line:
    points.append(random.normalvariate(0,point) + point)
figure = plt.figure(figsize = (12,6))
plt.rcParams['axes.ymargin'] = .05
plt.rcParams['axes.xmargin'] = .05
plt.plot(line, label = "Truth")


plt.scatter(np.arange(len(points)),points, s = 10, label = "Points from\nNormal Distribution") 
plt.title("Randomly Generated Points", fontsize = 16)

plt.legend(loc="Best")
plt.show()