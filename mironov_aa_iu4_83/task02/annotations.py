from collections import namedtuple

Tagged = namedtuple("Tagged", ["tag", "values", "color_name"])
Result = namedtuple("Step", ["z", "a"])
W_B = namedtuple("W_B", ["weights", "biases"])
Out = namedtuple("Out", ["name", "prob"])

