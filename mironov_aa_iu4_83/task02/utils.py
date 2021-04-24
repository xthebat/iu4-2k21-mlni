import numpy as np
from numpy import ndarray
import webcolors

from annotations import W_B
from config import neurons_in_hidden_layer, num_of_hidden_layers


# Some code from stackoverflow...
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.CSS3_HEX_TO_NAMES.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]


def get_color_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name


def hidden_layers():
    next_layers = [W_B(
        np.random.rand(neurons_in_hidden_layer, neurons_in_hidden_layer),   # weights
        np.random.rand(neurons_in_hidden_layer, 1)                          # bias
    ) for _ in range(num_of_hidden_layers - 1)]
    return next_layers


# f*ck u np
def to2d(x: ndarray) -> ndarray:
    return np.reshape(x, (x.size, 1)) if len(x.shape) == 1 else x


def glue(*args: ndarray, axis) -> ndarray:
    return np.concatenate(args, axis=axis)
