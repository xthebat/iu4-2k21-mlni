from collections import namedtuple
import random

import numpy as np
import imageio
from numpy import ndarray

from ext.function import rangend
from utils import to2d


class Dataset(object):

    def tags(self):
        raise NotImplementedError

    def batch(self, size) -> (ndarray, ndarray):
        raise NotImplementedError


class PictureDataset(Dataset):

    Tagged = namedtuple("Tagged", ["tag", "values"])

    def __init__(self, path: str):
        self.image = imageio.imread(path)
        data = dict()
        for row, col in rangend(self.image.shape[0], self.image.shape[1]):
            pixel = tuple(self.image[row][col])
            values = data.setdefault(pixel, list())
            values.append(np.array([row / self.image.shape[0], col / self.image.shape[1]]))

        self.data = [PictureDataset.Tagged(k, np.array(v)) for k, v in data.items()]
        print(f"Picture {path} loaded in dataset with total {len(self.tags())} classes")
        for tagged in self.data:
            print(f"Total data for {tagged.tag} class: {len(tagged.values)}")

    def tags(self):
        return [tagged.tag for tagged in self.data]

    def __batch_for_tag(self, tag_index, tagged, samples):
        total_x = len(tagged.values)
        indexes = random.sample(range(total_x), samples)
        x_data = np.array([tagged.values[index, :] for index in indexes])

        y_data = np.zeros(shape=(samples, len(self.tags())))
        y_data[:, tag_index] = 1

        return x_data, y_data

    def batch(self, size: int) -> (ndarray, ndarray):
        if size < len(self.tags()):
            index = random.randint(0, len(self.tags()) - 1)
            tagged = self.data[index]
            x_data, y_data = self.__batch_for_tag(index, tagged, 1)
            return x_data.T, y_data.T

        x_batch = []
        y_batch = []
        samples = int(size / len(self.tags()))
        for tag_index, tagged in enumerate(self.data):
            x_data, y_data = self.__batch_for_tag(tag_index, tagged, samples)
            x_batch.append(x_data)
            y_batch.append(y_data)

        x_batch = np.concatenate(x_batch)
        y_batch = np.concatenate(y_batch)

        return x_batch.T, y_batch.T
