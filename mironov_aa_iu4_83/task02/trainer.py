from typing import List, Optional, Callable

import numpy as np
from numpy import ndarray

from dataset import Dataset
from layers import Layer
from utils import to2d


class Trainer(object):

    def __init__(
            self,
            layers: List[Layer],
            batch_size: int,
            learning_rate: float,
            epochs: int,
            randomize_data: bool
    ):
        self.layers = layers
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.randomize_data = randomize_data

    def grads(self, x: ndarray, y: ndarray):
        z_s = []
        a_s = [x]
        for layer in self.layers:
            z, a = layer.forward(a_s[-1])
            z_s.append(z)
            a_s.append(a)

        deltas = [None] * len(self.layers)  # type: List[Optional[ndarray]]

        derivative = self.layers[-1].activation.backward(z_s[-1])
        deltas[-1] = (a_s[-1] - y) * derivative

        loss = np.abs(a_s[-1] - y).mean()

        for l in reversed(range(len(deltas) - 1)):
            derivative = self.layers[l].activation.backward(z_s[l])
            deltas[l] = self.layers[l + 1].weights.T @ deltas[l + 1] * derivative

        db = [delta.mean(axis=1) for delta in deltas]
        dw = [delta @ a_s[l].T / self.batch_size for l, delta in enumerate(deltas)]

        return loss, dw, db

    def epoch(self, index: int, x_batch: ndarray, y_batch: ndarray, on_learn: Callable):
        loss, d_weights, d_biases = self.grads(x_batch, y_batch)
        for layer, dw, db in zip(self.layers, d_weights, d_biases):
            layer.weights -= self.learning_rate * dw
            layer.bias -= self.learning_rate * to2d(db)
            # print(layer.weights)
            # print(layer.bias)
            # print(f"epoch={index} layer={layer} dw={dw.mean()} db={db.mean()} loss={loss}")
        on_learn(index, loss)

    def train(self, dataset: Dataset, on_learn):
        x_batch, y_batch = dataset.batch(self.batch_size)
        for epoch in range(self.epochs):
            self.epoch(epoch, x_batch, y_batch, on_learn)
            if self.randomize_data:
                x_batch, y_batch = dataset.batch(self.batch_size)

