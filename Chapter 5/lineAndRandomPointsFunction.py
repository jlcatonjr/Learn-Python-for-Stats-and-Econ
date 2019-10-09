#lineAndRandomPointsFunction.py
import numpy as np
import matplotlib.pyplot as plt
import random

def build_random_data_with_line(y_int, slope, SD = 1):

    # line is defined by the y_intercept and slope
    line = np.array([slope * (i + y_int) for i in range(100)])
    points = []
    for point in line:
        points.append(random.normalvariate(point, SD))
        
    return line, points

def plot_line(line, points, line_name = "Truth", 
              title = "Randomly Generated Points"):
    
    figure = plt.figure(figsize = (12,6))
    plt.rcParams['axes.ymargin'] = 0
    plt.rcParams['axes.xmargin'] = 0
    plt.plot(line, label = line_name)
    plt.scatter(np.arange(len(points)),points, s = 10, 
                label = "Points from\nNormal Distribution") 
    plt.title(title, fontsize = 20)
    plt.legend(loc="best")
    plt.show()
    
line, points = build_random_data_with_line(y_int = 3, slope = 1, SD = 10)
plot_line(line, points)