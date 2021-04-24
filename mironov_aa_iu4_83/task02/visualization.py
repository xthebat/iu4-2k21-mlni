from typing import List

import numpy as np
from matplotlib import pyplot as plt
import graphviz

from layers import Layer
from stats import Statistics


class Visualize:
    def __init__(self):
        pass

    @staticmethod
    def picture(inputs, outputs):
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        x = inputs[0, :]
        y = inputs[1, :]
        colors = [it.name for it in outputs.values()]

        ax.clear()
        ax.set_aspect('equal', 'box')
        plt.scatter(y, list(reversed(x)), c=colors)
        plt.pause(0.00001)

    def graphics(self, stats: Statistics, loss):
        self.parameter('Accuracy', stats.accuracy)
        self.parameter('Recall', stats.recall)
        self.parameter('Precision', stats.precision)
        self.parameter('F1 Score', stats.f1_score)
        self.loss(loss)

    @staticmethod
    def loss(loss):
        plt.axis([0, 50, 0, 100])
        plt.title('Pseudo loss')
        plt.plot(loss)
        plt.show()

    @staticmethod
    def parameter(title, parameter):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        if 'white' in parameter:
            ax.set_facecolor('gray')
        plt.title(title)
        for color in parameter:
            plt.plot(parameter[color], c=color)
        plt.show()

    @staticmethod
    def net(model: List[Layer]):
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

        for i, layer in enumerate(model):
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

        with d.subgraph(name=f'cluster_{len(model)}') as b:
            internal_layer = []
            node_name = 'o'
            b.attr(label='output layer', rank='same')
            b.node_attr.update(fillcolor='red1')
            for j in range(len(model[-1].weights)):
                internal_layer.append(f'{node_name}{len(model)}{j}')
                b.node(f'{node_name}{len(model)}{j}')
            _layers.append(internal_layer)

        for i in range(len(_layers) - 1):
            link_edges(d, _layers[i], _layers[i + 1], model[i].weights)

        d.render(filename='net.gv', directory="graph", view=True)
