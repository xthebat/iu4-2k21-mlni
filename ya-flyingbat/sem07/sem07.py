import numpy as np
from classifiers import LinearClassifier
from dataset import Dataset
from predictor import Predictor
from visualization import visualize, points


def example1():
    model = LinearClassifier(
        weights=np.array([
            [+1.0],
            [-1.0],
        ]),
        bias=np.array([0.0, 0.0])
    )
    results = Predictor(model, tags=["red", "green"]).predict(np.array([+10.0]))
    print(results)


def example2():
    model = LinearClassifier(
        weights=np.array([
            [+1.0],
            [-1.0],
            [-2.0]
        ]),
        bias=np.array([1.0, 2.0, 3.0])
    )
    results = Predictor(model, tags=["red", "green", "blue"]).predict(np.array([
        [+10.0, -0.1, -10.0],
    ]))
    print(results)


def example3():
    model = LinearClassifier(
        weights=np.array([
            [+5.0, +5.0],
            [-1.0, +3.0],
            [-2.0, -4.0]
        ]),
        bias=np.array([1.0, 2.0, 3.0])
    )
    results = Predictor(model, tags=["red", "green", "blue"]).predict(np.array([
        [+10.0, -0.1, -10.0],
        [+10.0, -0.1, -10.0]
    ]))
    print(results)


def example5():
    inputs = points(-1, 1, 20)

    model = LinearClassifier(
        weights=np.array([
            [+5.0, +5.0],
            [-1.0, +3.0],
            [-2.0, -4.0]
        ]),
        bias=np.array([1.0, 2.0, 3.0])
    )
    results = Predictor(model, tags=["red", "green", "blue"]).predict(inputs)
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
