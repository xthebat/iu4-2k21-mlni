from typing import List

import numpy as np
from numpy import ndarray

from activation import Softmax
from annotations import Out
from layers import Layer
from utils import to2d


class Predictor(object):

    def __init__(self, layers: List[Layer], tags: List[str], all_coordinates):
        assert layers[-1].outputs() == len(tags), "Number of model outputs must be equals to tags count"
        self.softmax = Softmax()
        self.layers = layers
        self.tags = tags
        self.all_coordinates = np.array(list(all_coordinates))

    def calc(self, x: ndarray) -> ndarray:
        a = x
        for layer in self.layers:
            _, a = layer.forward(a)
        return a

    def predict(self):
        inputs = np.transpose(self.all_coordinates)
        score = self.calc(to2d(inputs))
        prob = self.softmax.forward(score)
        indexes = np.argmax(prob, axis=0)
        return {
            (self.all_coordinates[k][0], self.all_coordinates[k][1]):
                Out(name=self.tags[out], prob=prob[out, k])
            for k, out in enumerate(indexes)
        }
