from typing import Dict, Tuple

from annotations import Out
from dataset import PictureDataset


class Statistics:
    def __init__(self, dataset: PictureDataset):
        self.colors = [data.color_name for data in dataset.data]
        self.real = dataset.tag_for_coordinate
        self.recall = {}
        self.precision = {}
        self.accuracy = {}
        self.f1_score = {}
        for color in self.colors:
            self.recall.setdefault(color, list())
            self.precision.setdefault(color, list())
            self.f1_score.setdefault(color, list())
            self.accuracy.setdefault(color, list())

    def calc_parameters(self, predicted: Dict[Tuple[float, float], Out]):
        for color in self.colors:
            TP = 0
            FN = 0
            FP = 0
            TN = 0
            for coord, out in predicted.items():
                actual = self.real[coord]
                pred = out.name

                if pred == color and actual == color:
                    TP += 1
                elif pred == color and actual != color:
                    FP += 1
                elif actual == color and pred != color:
                    FN += 1
                else:
                    TN += 1

            try:
                recall = TP / (TP + FN)
            except ZeroDivisionError:
                recall = 0
            try:
                precision = TP / (TP + FP)
            except ZeroDivisionError:
                precision = 0
            accuracy = (TP + TN) / (TP + TN + FN + FP)

            try:
                f1_score = 2*((precision * recall) / (precision + recall))
            except ZeroDivisionError:
                f1_score = 0

            self.recall[color].append(recall)
            self.precision[color].append(precision)
            self.f1_score[color].append(f1_score)
            self.accuracy[color].append(accuracy)
