import contextlib
from typing import List

import numpy as np
import pandas
from numpy import ndarray

from annotations import Tagged


@contextlib.contextmanager
def printoptions(*args, **kwargs):
    original = np.get_printoptions()
    np.set_printoptions(*args, **kwargs)
    try:
        yield
    finally:
        np.set_printoptions(**original)


class Statistics:
    def __init__(self, tags: List[Tagged]):
        self.colors = [tag.color for tag in tags]

    def print(self, predicted: ndarray, expected: ndarray):
        total_tags = len(self.colors)
        confusion_matrix, _, _ = np.histogram2d(expected, predicted, bins=np.arange(total_tags + 1))

        tp = confusion_matrix.diagonal()
        fp_tp = np.sum(confusion_matrix, axis=1)
        fn_tp = np.sum(confusion_matrix, axis=0)
        recall = tp / fp_tp
        precision = tp / fn_tp
        f1_score = 2 * ((precision * recall) / (precision + recall))

        print(pandas.DataFrame(confusion_matrix, dtype=int, columns=self.colors, index=self.colors))

        accuracy = np.sum(expected == predicted) / len(expected)
        print(f"accuracy: {accuracy}, metric:")

        with printoptions(formatter={'float': '{: 0.2f}'.format}):
            print(f"recall    = {recall}")
            print(f"precision = {precision}")
            print(f"f1_score  = {f1_score}")
