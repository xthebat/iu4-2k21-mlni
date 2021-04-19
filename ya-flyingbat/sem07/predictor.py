import numpy as np

from collections import namedtuple
from typing import List

from numpy import ndarray

from layers import Layer, Softmax
from utils import to2d

Out = namedtuple("Out", ["name", "prob"])


class Predictor(object):

    def __init__(self, layers: List[Layer], tags: List[str]):
        assert layers[-1].outputs() == len(tags), "Number of model outputs must be equals to tags count"
        self.softmax = Softmax()
        self.layers = layers
        self.tags = tags

    def calc(self, x: ndarray) -> ndarray:
        a = x
        for layer in self.layers:
            _, a = layer.forward(a)
        return a

    def predict(self, x: ndarray) -> List[Out]:
        score = self.calc(to2d(x))
        prob = self.softmax.forward(score)
        indexes = np.argmax(prob, axis=0)
        return [Out(name=self.tags[out], prob=prob[out, k]) for k, out in enumerate(indexes)]
