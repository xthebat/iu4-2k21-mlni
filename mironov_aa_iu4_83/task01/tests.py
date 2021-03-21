#!/home/andrey/MLNI/iu4-2k21-mlni/mironov_aa_iu4_83/env/bin/python
import unittest

from csv_utils import get_matrix
from dkstr import find_path
from main import scan_maze


class MazeTest(unittest.TestCase):

    def test_adjacency_matrix(self):
        expected = {(0, 1): 1, (1, 2): 2, (1, 3): 2, (3, 4): 8, (2, 4): 6}

        maze = get_matrix(filename='6x5.csv')

        adj_dict = {}
        paths = {}
        nodes = {}

        scan_maze(maze, adj_dict, paths, nodes)

        self.assertEqual(expected, adj_dict)

    def test_shortest_path(self):
        expected = 9

        path, length = find_path()
        self.assertEqual(expected, length)


if __name__ == '__main__':
    unittest.main()
