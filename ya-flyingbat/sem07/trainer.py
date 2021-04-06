from typing import List

from numpy import ndarray

from layers import Layer


class Backprop(object):

    def __init__(self, layers: List[Layer]):
        self.layers = layers