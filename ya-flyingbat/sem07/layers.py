import numpy as np

from numpy import ndarray

from utils import softmax, to2d


class Layer(object):

    def forward(self, x: ndarray) -> (ndarray, ndarray):
        raise NotImplementedError

    def backward(self, delta: ndarray, z: ndarray, a: ndarray) -> ndarray:
        raise NotImplementedError

    def inputs(self) -> int:
        raise NotImplementedError

    def outputs(self) -> int:
        raise NotImplementedError


class Activation(object):

    def forward(self, x: ndarray) -> ndarray:
        raise NotImplementedError


class Neuron(Layer):

    def __init__(self, weights: ndarray, bias: ndarray, activation: Activation):
        assert len(weights.shape) == 2, "Weight matrix must be 2-d"
        assert weights.shape[0] == len(bias), "Number of rows in weights must be equals to no. of outputs"
        self.weights = weights
        self.bias = to2d(bias)
        self.activation = activation

    def forward(self, x: ndarray) -> (ndarray, ndarray):
        b = np.tile(self.bias, (1, x.shape[1]))
        z = np.dot(self.weights, x) + b
        a = self.activation.forward(z)
        return z, a

    def backward(self, delta: ndarray, z: ndarray, a: ndarray) -> ndarray:
        return delta

    def inputs(self) -> int:
        return self.weights.shape[1]

    def outputs(self) -> int:
        return self.weights.shape[0]


class Sigmoid(Activation):

    def forward(self, x: ndarray) -> ndarray:
        return 1 / (1 + np.exp(-x))


class Softmax(Activation):

    def forward(self, x: ndarray) -> ndarray:
        return softmax(x)
