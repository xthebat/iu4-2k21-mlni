import numpy as np
from matplotlib import pyplot as plt


def points(start, end, n):
    inputs = []
    for x in np.linspace(start, end, n):
        for y in np.linspace(start, end, n):
            inputs.append((x, y))
    return np.array(inputs).transpose()


def visualize(inputs, outputs):
    x = inputs[0, :]
    y = inputs[1, :]
    colors = [it.name for it in outputs]
    plt.scatter(x, y, c=colors)
    plt.colorbar()
    plt.show()
