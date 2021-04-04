import numpy as np

from collections import namedtuple
from typing import List

from numpy import ndarray

from classifiers import Model


Out = namedtuple("Out", ["name", "prob"])


class Predictor(object):

    def __init__(self, model: Model, tags: List[str]):
        assert model.outputs() == len(tags), "Number of model outputs must be equals to tags count"
        self.model = model
        self.tags = tags

    def predict(self, x: ndarray) -> List[Out]:
        prob = self.model.prob(x)
        indexes = np.argmax(prob, axis=0)
        return [Out(name=self.tags[out], prob=prob[out, k]) for k, out in enumerate(indexes)]
