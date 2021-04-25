import numpy as np


class Activation(object):

    def forward(self, x: np.ndarray) -> np.ndarray:
        raise NotImplementedError

    def backward(self, z: np.ndarray) -> np.ndarray:
        raise NotImplementedError


class Sigmoid(Activation):

    def forward(self, x: np.ndarray) -> np.ndarray:
        return 1 / (1 + np.exp(-x))

    def backward(self, z: np.ndarray) -> np.ndarray:
        sigmoid = self.forward(z)
        return sigmoid * (1 - sigmoid)


class Softmax(Activation):

    def forward(self, x: np.ndarray) -> np.ndarray:
        return self.softmax(x)

    def backward(self, z: np.ndarray) -> np.ndarray:
        return np.ones(shape=z.shape)

    @staticmethod
    def softmax(x: np.ndarray) -> np.ndarray:
        return np.exp(x) / sum(np.exp(x))
        # return scipy.special.softmax(x)
