from typing import List

import graphviz
import matplotlib.pyplot as plt
import numpy as np

from layers import Layer
from predictor import Predictor


class LossPlotter:

    def __init__(self, axes):
        self.losses = list()
        self.axes = axes

    def append(self, loss):
        self.losses.append(loss)

    def plot(self):
        self.axes.clear()
        # self.axes.set_aspect('equal', 'box')
        self.axes.plot(self.losses, "--o")


def points(start, end, n):
    inputs = []
    for x in np.linspace(start, end, n):
        for y in np.linspace(start, end, n):
            inputs.append((x, y))
    return np.array(inputs).transpose()


class ClassSeparationPlotter:

    def __init__(self, axes, tags: List, predictor: Predictor):
        self.axes = axes
        self.tags = tags
        self.predictor = predictor
        self.inputs = points(0, 1.0, 30)

    def draw(self):
        outputs, _ = self.predictor.predict(self.inputs)
        x = list(reversed(self.inputs[0, :]))
        y = self.inputs[1, :]
        colors = [np.array(self.tags[index].tag) / 256 for index in outputs]
        self.axes.clear()
        self.axes.set_aspect('equal', 'box')
        self.axes.scatter(y, x, c=colors)


class NeuralNetworkVisualizer:

    def __init__(self, model: List[Layer], axes):
        self.model = model
        self.axes = axes

    def draw(self):
        d = graphviz.Digraph()

        def calc_color(i, j, weights):
            weights -= np.min(weights)
            percent = int((weights[j][i] / np.max(weights)) * 100)
            return f"gray{100 - percent}"

        def link_edges(d, starts, ends, weights):
            for i_idx, i in enumerate(starts):
                for j_idx, j in enumerate(ends):
                    d.edge(i, j, color=calc_color(i_idx, j_idx, weights))

        d.attr(rankdir='LR', penwidth='0', splines='line', nodesep='1')
        d.attr('node', shape='circle', style='filled', fixedsize='true')
        d.attr('edge', arrowhead="none")

        _layers = []

        for i, layer in enumerate(self.model):
            internal_layer = []
            with d.subgraph(name=f'cluster_{i}') as a:
                if i == 0:
                    node_name = 'i'
                    a.attr(label='input layer', rank='same')
                    a.node_attr.update(fillcolor='darkseagreen1')
                else:
                    node_name = 'h'
                    a.attr(label='hidden layer', rank='same')
                    a.node_attr.update(fillcolor='cadetblue1')

                for j in range(len(np.transpose(layer.weights))):
                    internal_layer.append(f'{node_name}{i}{j}')
                    a.node(f'{node_name}{i}{j}')

            _layers.append(internal_layer)

        with d.subgraph(name=f'cluster_{len(self.model)}') as b:
            internal_layer = []
            node_name = 'o'
            b.attr(label='output layer', rank='same')
            b.node_attr.update(fillcolor='red1')
            for j in range(len(self.model[-1].weights)):
                internal_layer.append(f'{node_name}{len(self.model)}{j}')
                b.node(f'{node_name}{len(self.model)}{j}')
            _layers.append(internal_layer)

        for i in range(len(_layers) - 1):
            link_edges(d, _layers[i], _layers[i + 1], self.model[i].weights)

        d.render(filename='net', directory="graph", format="png", view=False)
        picture = plt.imread('graph/net.png')
        self.axes.clear()
        self.axes.imshow(picture)
        self.axes.set_aspect('equal', 'box')
        self.axes.axis('off')

