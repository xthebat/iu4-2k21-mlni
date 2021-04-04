import unittest
from collections import namedtuple
from typing import Optional, Set, Tuple, List

import imageio
from imageio.core import Array

from ext.function import rangend

Result = namedtuple("Result", ["color", "cells"])


def neighbours(image: Array, row: int, col: int):
    rows, cols, _ = image.shape
    for drow, dcol in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        next_row = row + drow
        next_col = col + dcol
        if 0 <= next_row < rows and 0 <= next_col < cols:
            yield next_row, next_col


def fill_up_one(image: Array, row: int, col: int, visited: Optional[Set[Tuple]] = None) -> Set[Tuple]:
    visited = visited or set()
    current = row, col
    if current in visited:
        return visited
    visited.add(current)
    color = image[row][col]  # type: Array
    for neighbour_row, neighbour_col in neighbours(image, row, col):
        if all(image[neighbour_row][neighbour_col] == color):
            fill_up_one(image, neighbour_row, neighbour_col, visited)
    return visited


def fill_up_all(image):
    visited = set()
    for row, col in rangend(image.shape[0], image.shape[1]):
        if (row, col) not in visited:
            cells = fill_up_one(image, row, col)
            visited.update(cells)
            yield Result(list(image[row][col]), sorted(cells))


def fill_up_max(image):
    return max(fill_up_all(image), key=lambda it: len(it.cells))


class Fillup(unittest.TestCase):

    def test_neighbours_corner(self):
        image = imageio.imread("sem05_01.png")
        actual = list(neighbours(image, 0, 0))
        expected = [(1, 0), (0, 1)]
        self.assertEqual(expected, actual)

    def test_neighbours_middle(self):
        image = imageio.imread("sem05_01.png")
        actual = list(neighbours(image, 1, 1))
        expected = [(0, 1), (2, 1), (1, 0), (1, 2)]
        self.assertEqual(expected, actual)

    def test_fill_up_one_cyan_pic_01(self):
        image = imageio.imread("sem05_01.png")
        actual = sorted(fill_up_one(image, 0, 0))
        expected = [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 4), (2, 4), (3, 4)]
        self.assertEqual(expected, actual)

    def test_fill_up_one_green_pic_01(self):
        image = imageio.imread("sem05_01.png")
        actual = sorted(fill_up_one(image, 1, 2))
        expected = [(1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]
        self.assertEqual(expected, actual)

    def test_painting_pic_01(self):
        image = imageio.imread("sem05_01.png")
        actual = list(fill_up_all(image))
        expected = [
            Result(color=[0, 255, 255],
                   cells=[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 4), (2, 4), (3, 4)]),
            Result(color=[0, 255, 0], cells=[(1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]),
            Result(color=[255, 128, 0], cells=[(2, 0), (3, 0)]),
            Result(color=[255, 0, 0], cells=[(2, 1)]),
            Result(color=[0, 255, 255], cells=[(3, 1)]),
            Result(color=[255, 0, 0], cells=[(3, 2)])]
        self.assertEqual(expected, actual)

    def test_painting_max_pic_01(self):
        image = imageio.imread("sem05_01.png")
        actual = fill_up_max(image)
        self.assertEqual(10, len(actual.cells))
