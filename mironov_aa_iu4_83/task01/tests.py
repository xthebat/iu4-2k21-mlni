#!/home/andrey/MLNI/iu4-2k21-mlni/mironov_aa_iu4_83/env/bin/python
import unittest

from csv_utils import get_matrix
from dkstr import shortest_path
from models import Maze


class MazeTest(unittest.TestCase):

    def test_adjacency_matrix(self):
        # expected = {(0, 1): 1, (1, 2): 2, (1, 3): 2, (3, 2): 4, (3, 4): 8, (2, 4): 6}
        # after review: results are the same just differ order
        expected = {(0, 1): 1, (1, 2): 2, (1, 3): 2, (2, 3): 4, (2, 4): 6, (3, 4): 8}

        matrix = get_matrix(filename='6x5.csv')

        maze = Maze(matrix)

        self.assertEqual(expected, maze.adjacency)

    def test_shortest_path(self):
        expected = 9

        path, length = shortest_path()
        self.assertEqual(expected, length)


if __name__ == '__main__':
    unittest.main()
