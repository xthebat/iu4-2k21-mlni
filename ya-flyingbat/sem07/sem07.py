import numpy as np
from layers import Neuron, Softmax
from dataset import Dataset
from predictor import Predictor
from utils import to2d
from visualization import visualize, points


def example1():
    model = Neuron(
        weights=np.array([
            [+1.0],
            [-1.0],
        ]),
        bias=np.array([0.0, 0.0]),
        activation=Softmax()
    )
    results = Predictor([model], tags=["red", "green"]).predict(np.array([+10.0]))
    print(results)


def example2():
    model = Neuron(
        weights=np.array([
            [+1.0],
            [-1.0],
            [-2.0]
        ]),
        bias=np.array([1.0, 2.0, 3.0]),
        activation=Softmax()
    )
    results = Predictor([model], tags=["red", "green", "blue"]).predict(np.array([
        [+10.0, -0.1, -10.0],
    ]))
    print(results)


def example3():
    model = Neuron(
        weights=np.array([
            [+5.0, +5.0],
            [-1.0, +3.0],
            [-2.0, -4.0]
        ]),
        bias=np.array([1.0, 2.0, 3.0]),
        activation=Softmax()
    )
    results = Predictor([model], tags=["red", "green", "blue"]).predict(np.array([
        [+10.0, -0.1, -10.0],
        [+10.0, -0.1, -10.0]
    ]))
    print(results)


def example5():
    inputs = points(-1, 1, 20)

    model = Neuron(
        weights=np.array([
            [+5.0, +5.0],
            [-1.0, +3.0],
            [-2.0, -4.0]
        ]),
        bias=to2d(np.array([1.0, 2.0, 3.0])),
        activation=Softmax()
    )
    results = Predictor([model], tags=["red", "green", "blue"]).predict(inputs)
    print("Visualizing...")
    visualize(inputs, results)


def main():
    dataset = Dataset()

    # example1()
    # example2()
    # example3()
    example5()


if __name__ == '__main__':
    main()
