import numpy as np
from matplotlib import pyplot as plt

from activation import Sigmoid, Softmax
from config import filename, visualize_only_in_the_end, learning_rate
from dataset import PictureDataset
from layers import Layer, weights_and_biases
from predictor import Predictor
from stats import Statistics
from trainer import Trainer
from visualization import Visualize

dataset = PictureDataset(f"pictures/{filename}.png")


def memoize_on_learn(predictor: Predictor, stats: Statistics, visualize: Visualize):

    def on_learn():
        predicted = predictor.predict()
        stats.calc_parameters(predicted)

        if not visualize_only_in_the_end:
            visualize.picture(np.transpose(predictor.all_coordinates), predicted)

        return predicted

    return on_learn


def main():
    w_b = weights_and_biases(dataset)

    model = [Layer(
        weights=v.weights,
        bias=v.biases,
        activation=Sigmoid() if layer_index != len(w_b) - 1 else Softmax()
    ) for layer_index, v in enumerate(w_b)]

    trainer = Trainer(model)
    predictor = Predictor(
        model,
        tags=[i.color_name for i in dataset.data],
        all_coordinates=dataset.tag_for_coordinate.keys()
    )

    stats = Statistics(dataset)
    visualize = Visualize()

    on_learn = memoize_on_learn(predictor, stats, visualize)

    try:
        trainer.train(dataset, lr=learning_rate, on_learn=on_learn)
    except KeyboardInterrupt:
        print("Training interrupted... storing weights")
    finally:
        for index, layer in enumerate(model):
            np.save(f"w&b/{index}_weights.npy", layer.weights)
            np.save(f"w&b/{index}_bias.npy", layer.bias)

        visualize.picture(np.transpose(predictor.all_coordinates), on_learn())
        visualize.graphics(stats, trainer.loss)
        visualize.net(model)


if __name__ == '__main__':
    main()
