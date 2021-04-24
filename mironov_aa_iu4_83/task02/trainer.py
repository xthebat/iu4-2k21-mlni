from collections import namedtuple
from typing import List, Optional

import numpy as np
from numpy import ndarray

from dataset import Dataset
from layers import Layer
from activation import Softmax
from config import visualize_only_in_the_end, epochs, batch_size
from utils import to2d


class Trainer(object):

    def __init__(self, layers: List[Layer]):
        self.layers = layers
        self.batch_size = batch_size
        self.softmax = Softmax()
        self.loss = []
        self.recall = []
        self.precision = []

    def grads(self, x: ndarray, y: ndarray):
        z_s = []
        a_s = [x]
        for layer in self.layers:
            z, a = layer.forward(a_s[-1])
            z_s.append(z)
            a_s.append(a)

        deltas: List[Optional[ndarray]] = [None] * len(self.layers)

        derivative = self.layers[-1].activation.backward(z_s[-1])
        deltas[-1] = (a_s[-1] - y) * derivative

        loss = np.abs(a_s[-1] - y).mean()

        for l in reversed(range(len(deltas) - 1)):
            derivative = self.layers[l].activation.backward(z_s[l])
            deltas[l] = self.layers[l + 1].weights.T @ deltas[l + 1] * derivative

        db = [delta.mean(axis=1) for delta in deltas]
        dw = [delta @ a_s[l].T / self.batch_size for l, delta in enumerate(deltas)]

        return loss, dw, db

    def epoch(self, index: int, x_batch: ndarray, y_batch: ndarray, lr: float, on_learn):
        loss, d_weights, d_biases = self.grads(x_batch, y_batch)
        for layer, dw, db in zip(self.layers, d_weights, d_biases):
            layer.weights -= lr * dw
            layer.bias -= lr * to2d(db)
        if index % (epochs // 500) == 0:
            loss = loss * 100
            print("================ epoch={:5} loss={:3.2f}% ================".format(index, loss))
        if index % (epochs // 50) == 0:
            on_learn()
            self.loss.append(loss)

    def train(self, dataset: Dataset, lr: float, on_learn):
        for epoch in range(epochs):
            x_batch, y_batch = dataset.batch(self.batch_size)
            self.epoch(epoch, x_batch, y_batch, lr, on_learn)
