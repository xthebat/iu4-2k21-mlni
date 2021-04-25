from collections import namedtuple

Tagged = namedtuple("Tagged", ["index", "tag", "values", "color"])
Result = namedtuple("Step", ["z", "a"])
W_B = namedtuple("W_B", ["weights", "biases"])
Out = namedtuple("Out", ["tag", "prob"])

