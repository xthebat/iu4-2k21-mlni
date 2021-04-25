import random
from typing import Optional, List, Tuple, Iterable

import imageio
import numpy as np
from numpy import ndarray

from annotations import Tagged
from ext.function import rangend
from utils import get_color_name


class Dataset(object):

    def tags(self) -> List[Tagged]:
        raise NotImplementedError

    def batch(self, size: Optional[int] = None) -> (ndarray, ndarray):
        raise NotImplementedError


class PictureDataset(Dataset):

    def __init__(self, path: str):
        self.image = imageio.imread(path)
        data = dict()
        for row, col in rangend(self.image.shape[0], self.image.shape[1]):
            pixel = tuple(self.image[row][col])
            values = data.setdefault(pixel, list())
            coordinate = (row / self.image.shape[0], col / self.image.shape[1])
            values.append(np.array(coordinate))

        self.data = [Tagged(index, rgb, np.array(values), get_color_name(rgb))
                     for index, (rgb, values) in enumerate(data.items())]

        print(f"Picture {path} loaded in dataset with total {len(self.tags())} classes")
        for tagged in self.data:
            print(f"Total data for {tagged.color} class: {len(tagged.values)}")

    def tags(self) -> List[Tagged]:
        return self.data

    def __batch_for_tag(self, tagged: Tagged, samples: Optional[int] = None):
        total_x = len(tagged.values)
        samples = samples or total_x
        indexes = random.sample(range(total_x), samples)
        x_data = np.array([tagged.values[index, :] for index in indexes])

        y_data = np.zeros(shape=(samples, len(self.tags())))
        y_data[:, tagged.index] = 1

        return x_data, y_data

    def __batch(self, sizes: Iterable[Tuple[Tagged, int]]) -> (ndarray, ndarray):
        x_batch = []
        y_batch = []
        for tagged, samples in sizes:
            x_data, y_data = self.__batch_for_tag(tagged, samples)
            x_batch.append(x_data)
            y_batch.append(y_data)

        x_batch = np.concatenate(x_batch)
        y_batch = np.concatenate(y_batch)

        return x_batch.T, y_batch.T

    def batch(self, size: Optional[int] = None) -> (ndarray, ndarray):
        if size is None:
            return self.__batch((tagged, len(tagged.values)) for tagged in self.data)

        elif size < len(self.tags()):
            tagged = random.choice(self.data)
            x_data, y_data = self.__batch_for_tag(tagged, size)
            return x_data.T, y_data.T

        else:
            samples = int(size / len(self.tags()))
            return self.__batch((tagged, samples) for tagged in self.data)

