from typing import Optional

import numpy as np
from matplotlib import pyplot as plt

from activation import Sigmoid, Softmax
from config import filename, visualize_only_at_the_end, learning_rate, batch_size, epochs, randomize_data
from dataset import PictureDataset, Dataset
from layers import Layer, weights_and_biases
from predictor import Predictor
from stats import Statistics
from trainer import Trainer
from visualization import NeuralNetworkVisualizer, LossPlotter, ClassSeparationPlotter


def memoize_on_learn(
        dataset: Dataset,
        predictor: Predictor,
        stats: Statistics,
        nn_visualizer: NeuralNetworkVisualizer,
        loss_plotter: LossPlotter,
        class_plotter: ClassSeparationPlotter
):

    inputs, expected_matrix = dataset.batch(None)  # get whole dataset

    def on_learn(index: int, loss: Optional[float]):
        if index != -1:
            if index % 5000 != 0:
                return

            loss_plotter.append(loss)

            print(f"================ epoch={index} loss={loss} ================")

        predicted, _ = predictor.predict(inputs)

        expected = np.argmax(expected_matrix, axis=0)  # convert to flat view
        stats.print(predicted, expected)

        if not visualize_only_at_the_end:
            loss_plotter.plot()
            class_plotter.draw()
            nn_visualizer.draw()
            plt.pause(0.001)

        return predicted

    return on_learn


def main():
    dataset = PictureDataset(f"pictures/{filename}.png")

    w_b = weights_and_biases(dataset)

    model = [Layer(
        weights=v.weights,
        bias=v.biases,
        activation=Sigmoid() if index != len(w_b) - 1 else Softmax()
    ) for index, v in enumerate(w_b)]

    predictor = Predictor(model, dataset.tags())

    figure = plt.figure()

    stats = Statistics(dataset.tags())
    nn_visualizer = NeuralNetworkVisualizer(model, figure.add_subplot(1, 3, 1))
    loss_plotter = LossPlotter(figure.add_subplot(1, 3, 2))
    class_plotter = ClassSeparationPlotter(figure.add_subplot(1, 3, 3), dataset.tags(), predictor)

    figure.tight_layout()

    on_learn = memoize_on_learn(dataset, predictor, stats, nn_visualizer, loss_plotter, class_plotter)

    try:
        trainer = Trainer(
            model,
            learning_rate=learning_rate,
            batch_size=batch_size,
            epochs=epochs,
            randomize_data=randomize_data)
        trainer.train(dataset, on_learn=on_learn)
    except KeyboardInterrupt:
        print("Training interrupted... storing weights")
    finally:
        for index, layer in enumerate(model):
            np.save(f"w&b/{index}_weights.npy", layer.weights)
            np.save(f"w&b/{index}_bias.npy", layer.bias)

        on_learn(-1, None)

        class_plotter.draw()
        loss_plotter.plot()
        nn_visualizer.draw()


if __name__ == '__main__':
    main()
