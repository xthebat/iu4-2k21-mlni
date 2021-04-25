import numpy as np
from numpy import ndarray

from activation import Activation
from annotations import W_B
from config import load_previous_session, num_of_hidden_layers, neurons_in_hidden_layer
from utils import to2d, hidden_layers


class Layer:

    def __init__(self, weights: ndarray, bias: ndarray, activation: Activation):
        assert len(weights.shape) == 2, "Weight matrix must be 2-d"
        # assert weights.shape[0] == len(bias), "Number of rows in weights must be equals to no. of outputs"
        self.weights = weights
        self.bias = to2d(bias)
        self.activation = activation

    def forward(self, x: ndarray) -> (ndarray, ndarray):
        x = to2d(x)
        b = np.tile(self.bias, (1, x.shape[1]))
        z = self.weights @ x + b
        a = self.activation.forward(z)
        return z, a

    def inputs(self) -> int:
        return self.weights.shape[1]

    def outputs(self) -> int:
        return self.weights.shape[0]


def weights_and_biases(dataset):
    w_b = []
    if load_previous_session:
        for index in range(num_of_hidden_layers + 1):
            weighs = np.load(f"w&b/{index}_weights.npy")
            bias = np.load(f"w&b/{index}_bias.npy")
            w_b.append(W_B(weighs, bias))
    else:
        input_layer = W_B(
            np.random.rand(neurons_in_hidden_layer, 2),                 # two inputs: x1, x2
            np.random.rand(neurons_in_hidden_layer, 1)
        )

        hidden = hidden_layers()

        output_layer = W_B(
            np.random.rand(len(dataset.data), neurons_in_hidden_layer),
            np.random.rand(len(dataset.data), 1)
        )

        w_b = [input_layer] + hidden + [output_layer]

    return w_b
