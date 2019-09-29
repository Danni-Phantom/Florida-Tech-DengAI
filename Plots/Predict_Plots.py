import numpy as np
import matplotlib.pyplot as plt
from scipy import stats


def corr_plot(x, x_name, y, y_name, graph_name):
    plt.figure()
    plt.scatter(x, y)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.title(graph_name)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    abline(slope, intercept)
    plt.plot()


def abline(slope, intercept):
    axes = plt.gca()
    x_vals = np.array(axes.get_xlim())
    y_vals = intercept + slope * x_vals
    plt.plot(x_vals, y_vals)
