import numpy as np

from numpy import ndarray

from utils import softmax, to2d


class Model(object):

    def prob(self, x: ndarray) -> ndarray:
        raise NotImplementedError

    def inputs(self) -> int:
        raise NotImplementedError

    def outputs(self) -> int:
        raise NotImplementedError


class NearestNeighbour(Model):

    def prob(self, x: ndarray) -> ndarray:
        pass

    def inputs(self) -> int:
        pass

    def outputs(self) -> int:
        pass


class LinearClassifier(Model):

    def __init__(self, weights: ndarray, bias: ndarray):
        assert len(weights.shape) == 2, "Weight matrix must be 2-d"
        assert weights.shape[0] == len(bias), "Number of rows in weights must be equals to no. of outputs"
        self.weights = weights
        self.bias = to2d(bias)

    def prob(self, x: ndarray) -> ndarray:
        x = to2d(x)
        b = np.tile(self.bias, (1, x.shape[1]))
        y = np.dot(self.weights, x) + b
        return softmax(y)

    def inputs(self) -> int:
        return self.weights.shape[1]

    def outputs(self) -> int:
        return self.weights.shape[0]

