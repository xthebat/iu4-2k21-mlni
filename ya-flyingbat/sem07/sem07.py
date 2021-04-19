import time

import numpy as np
from layers import Neuron, Softmax, Sigmoid
from dataset import Dataset, PictureDataset
from predictor import Predictor
from trainer import Trainer
from utils import to2d
from visualization import visualize, points
from matplotlib import pyplot as plt



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
    inputs = points(-1, 1, 30)

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


dataset = PictureDataset("temp/2.png")

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111)


def on_learn(model):
    inputs = points(0, 1.0, 60)
    results = Predictor(model, tags=["red", "green", "blue", "black", "brown", "yellow"]).predict(inputs)
    ax.clear()
    visualize(inputs, results)
    plt.pause(0.00001)


np.set_printoptions(precision=6, suppress=True)


def example6():
    # weights_and_biases = []
    # for index in range(3):
    #     weighs = np.load(f"temp/{index}_weights.npy")
    #     bias = np.load(f"temp/{index}_bias.npy")
    #     weights_and_biases.append((weighs, bias))

    # weights_and_biases = [
    #     (np.random.rand(4, 2), np.random.rand(4, 1)),
    #     (np.random.rand(4, 4), np.random.rand(4, 1)),
    #     (np.random.rand(6, 4), np.random.rand(6, 1))
    # ]

    # time.sleep(1.0)

    # weights_and_biases = [
    #     (np.random.rand(6, 2), np.random.rand(6, 1))
    # ]

    weights_and_biases = [
        (np.random.rand(4, 2), np.random.rand(4, 1)),
        (np.random.rand(6, 4), np.random.rand(6, 1))
    ]

    model = [Neuron(weights=v[0], bias=v[1], activation=Sigmoid()) for v in weights_and_biases]
    model[-1].activation = Softmax()

    inputs = points(0, 1.0, 30)
    results = Predictor(model, tags=["red", "green", "blue", "black", "brown", "yellow"]).predict(inputs)
    visualize(inputs, results)

    trainer = Trainer(model, batch_size=6 * 100)
    try:
        trainer.train(dataset, epochs=100000, lr=0.1, on_learn=on_learn)
    finally:
        print("Training interrupted... storing weights")
        for index, layer in enumerate(model):
            np.save(f"temp/{index}_weights.npy", layer.weights)
            np.save(f"temp/{index}_bias.npy", layer.bias)


def main():
    # example1()
    # example2()
    # example3()
    # example5()
    example6()


if __name__ == '__main__':
    main()
