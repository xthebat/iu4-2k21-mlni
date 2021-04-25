from typing import List

import numpy as np
from numpy import ndarray

from annotations import Tagged
from layers import Layer
from utils import to2d


class Predictor(object):

    def __init__(self, layers: List[Layer], tags: List[Tagged]):
        self.layers = layers
        self.tags = tags

    def calc(self, x: ndarray) -> ndarray:
        a = x
        for layer in self.layers:
            _, a = layer.forward(a)
        return a

    def predict(self, x: ndarray) -> (ndarray, ndarray):
        prob = self.calc(to2d(x))
        indexes = np.argmax(prob, axis=0)
        return indexes, np.max(prob, axis=0)
