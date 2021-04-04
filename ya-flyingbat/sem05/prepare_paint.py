import unittest
from collections import namedtuple
from typing import Tuple, Optional, Set, List

import imageio
from imageio.core import Array

from ext.function import rangend

Result = namedtuple("Result", ["color", "cells"])


def is_color_equals(this: Array, other: Array or List):
    return all(this == other)


def neighbours(image, row, col):
    rows = image.shape[0]
    cols = image.shape[1]
    for drow, dcol in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
        next_row = row + drow
        next_col = col + dcol
        if 0 <= next_row < rows and 0 <= next_col < cols:
            yield next_row, next_col


def fill_up_one(image, row, col, visited: Optional[Set[Tuple]] = None):
    visited = visited or set()
    if (row, col) in visited:
        return visited
    visited.add((row, col))

    color = image[row][col]

    for next_row, next_col in filter(
            lambda rc: is_color_equals(image[rc[0]][rc[1]], color),
            neighbours(image, row, col)
    ):
        fill_up_one(image, next_row, next_col, visited)

    return visited


def fill_up_all(image):
    return map(
        lambda rc: Result(image[rc[0]][rc[1]], fill_up_one(image, rc[0], rc[1])),
        rangend(image.shape[0], image.shape[1])
    )


def find_max_fill(image):
    return max(fill_up_all(image), key=lambda it: len(it.cells))  # type: Result


class TestLambda(unittest.TestCase):

    def test_pic_01(self):
        result = find_max_fill(imageio.imread("sem05_01.png"))
        print(result.color, len(result.cells))
        self.assertTrue(is_color_equals(result.color, [0, 255, 255]))

    def test_pic_02(self):
        result = find_max_fill(imageio.imread("sem05_02.png"))
        print(result.color, len(result.cells))
        self.assertTrue(is_color_equals(result.color, [0, 255, 0]))


# def main():
#     image = imageio.imread("sem05_02.png")
#     result = find_max_fill(image)
#     print(result.color, len(result.cells))
#
#
# if __name__ == '__main__':
#     main()
