import numpy as np

from collections import namedtuple
from typing import List, Optional

from numpy import ndarray

from dataset import Dataset
from layers import Layer, Neuron, Softmax
from utils import to2d

Result = namedtuple("Step", ["z", "a"])


class Trainer(object):

    def __init__(self, layers: List[Neuron], batch_size):
        self.layers = layers
        self.batch_size = batch_size
        self.softmax = Softmax()

    def grads(self, x: ndarray, y: ndarray):
        z_s = []
        a_s = [x]
        for l, layer in enumerate(self.layers):
            z, a = layer.forward(a_s[-1])
            z_s.append(z)
            a_s.append(a)

        deltas = [None] * len(self.layers)  # type: List[Optional[ndarray]]

        deriv = self.layers[-1].activation.backward(z_s[-1])
        deltas[-1] = (a_s[-1] - y) * deriv

        # for k in range(x.shape[1]):
        #     q0 = " ".join(["%.2f" % v for v in x[:, k]])
        #     q1 = " ".join(["%1d" % v for v in y[:, k]])
        #     q2 = " ".join(["%.2f" % v for v in a_s[-1][:, k]])
        #     print(f"x={q0} => y={q1} a={q2}")

        loss = np.abs(a_s[-1] - y).mean()

        for l in reversed(range(len(deltas) - 1)):
            deriv = self.layers[l].activation.backward(z_s[l])
            deltas[l] = self.layers[l + 1].weights.T @ deltas[l + 1] * deriv

        db = [delta.mean(axis=1) for delta in deltas]
        dw = [delta @ a_s[l].T / self.batch_size for l, delta in enumerate(deltas)]

        # for k, (q0, q1) in enumerate(zip(dw, db)):
        #     print(f"Layer {k} change:")
        #     print(q0)
        #     print(q1)

        return loss, dw, db

    def epoch(self, index: int, x_batch: ndarray, y_batch: ndarray, lr: float, on_learn):
        loss, dweights, dbiases = self.grads(x_batch, y_batch)
        for layer, dw, db in zip(self.layers, dweights, dbiases):
            layer.weights -= lr * dw
            layer.bias -= lr * to2d(db)
            # print(layer.weights)
            # print(layer.bias)
            # print(f"epoch={index} layer={layer} dw={dw.mean()} db={db.mean()} loss={loss}")
        if index % 200 == 0:
            print(f"================ epoch={index} loss={loss} ================")
            on_learn(self.layers)

    def train(self, dataset: Dataset, epochs: int, lr: float, on_learn):
        for epoch in range(epochs):
            x_batch, y_batch = dataset.batch(self.batch_size)
            self.epoch(epoch, x_batch, y_batch, lr, on_learn)
