#lineAndRandomPoints.py
import numpy as np
import matplotlib.pyplot as plt
import random

# create a function that plots a line with random points around it
# include options in the function that if not included use a default
#      funct(keyword = default)
def plot_line_with_random_points(line = None, sigma = 100, figsize = (12,6),
                                 s = 10, legend = True, legend_loc= "upper left",
                                 alpha = .5, legend_fontsize = 20, 
                                 bbox_to_anchor=(0, 1.38)):
    # if no line passed, then create a line
    if line is None:
        line = np.array([i + 3 for i in range(100)])
    # make figsize the value passed as figsize
    figure = plt.figure(figsize = figsize)
    # reduce excess margins
    plt.rcParams['axes.ymargin'] = 0
    plt.rcParams['axes.xmargin'] = 0
    # plot line, include label for line if legend is called
    plt.plot(line, label = "Truth")  
    # create one random point for every point in line
    points = []
    for point in line:
        # appends random points generate using line as mean
        points.append(random.normalvariate(point, sigma = sigma))
    # plot the random points generated
    plt.scatter(np.arange(len(points)), points, s = s, alpha = alpha,
                label = "Points from\nNormal Distribution" )
    # if legend option is True, create legend
    if legend == True:
        # at function level, you may choose legend_loc
        plt.legend(loc = legend_loc, fontsize = legend_fontsize, 
                   bbox_to_anchor = bbox_to_anchor)
    plt.show()

quadratic = np.array([-i**2 +  100 * i + 100 for i in range(200)])
plot_line_with_random_points(quadratic, 5000, s = 10, legend = True, 
                             figsize = (10,5), alpha = 1)
plot_line_with_random_points(quadratic)