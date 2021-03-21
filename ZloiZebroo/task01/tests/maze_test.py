import unittest
from task01 import maze as graph


class MazeTests(unittest.TestCase):

    def test_graph_02(self):
        data = graph.load_from_txt('../maze_02.txt')
        actual = [data.nodes, data.adj, data.adj_matrix, data.matrix.data]
        expected = [
            {0: [0, 0], 1: [1, 2], 2: [9, 4], 3: [9, 2], 4: [9, 5], 5: [9, 0]},
            {0: {1: 3},
             1: {0: 3, 2: 10, 3: 8},
             2: {1: 10, 3: 2, 4: 1},
             3: {1: 8, 2: 2, 5: 2},
             4: {2: 1},
             5: {3: 2}},
            [[None, 3, None, None, None, None],
             [3, None, 10, 8, None, None],
             [None, 10, None, 2, 1, None],
             [None, 8, 2, None, None, 2],
             [None, None, 1, None, None, None],
             [None, None, None, 2, None, None]],
            [['1', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
             ['0', '1', '0', '0', '0', '0', '0', '0', '0', '1'],
             ['0', '1', '1', '1', '1', '1', '1', '1', '1', '1'],
             ['0', '0', '0', '0', '0', '0', '0', '0', '0', '1']],
        ]
        self.assertEqual(expected, actual)

    def test_load_from_json(self):
        data = graph.load_from_json('maze_graph.json')
        actual = [data.nodes, data.adj, data.adj_matrix]
        expected = [
            {'0': [0, 0], '1': [1, 2], '2': [9, 4], '3': [9, 2], '4': [9, 5], '5': [9, 0]},
            {'0': {'1': 2}, '1': {'0': 2, '2': 9, '3': 7}, '2': {'1': 9, '4': 0, '3': 1}, '3': {'1': 7, '2': 1, '5': 1}, '4': {'2': 0}, '5': {'3': 1}},
            [[None, 2, None, None, None, None], [2, None, 9, 7, None, None], [None, 9, None, 1, 0, None],
             [None, 7, 1, None, None, 1], [None, None, 0, None, None, None], [None, None, None, 1, None, None]]
        ]
        self.assertEqual(expected, actual)

    def test_graph_2x2(self):
        data = graph.load_from_txt('../maze_04.txt')
        actual = [data.nodes, data.adj, data.adj_matrix]
        expected = [
            {},
            {},
            []
        ]
        self.assertEqual(expected, actual)

    def test_graph_3x3(self):
        data = graph.load_from_txt('../maze_03.txt')
        actual = [data.nodes, data.adj, data.adj_matrix]
        expected = [
            {0: [1, 0], 1: [1, 1], 2: [0, 1], 3: [2, 1], 4: [1, 2]},
            {0: {1: 1, 2: 2, 3: 2},
             1: {0: 1, 2: 1, 3: 1, 4: 1},
             2: {0: 2, 1: 1, 4: 2},
             3: {0: 2, 1: 1, 4: 2},
             4: {1: 1, 2: 2, 3: 2}},
            [[None, 1, 2, 2, None],
             [1, None, 1, 1, 1],
             [2, 1, None, None, 2],
             [2, 1, None, None, 2],
             [None, 1, 2, 2, None]]
        ]
        self.assertEqual(expected, actual)

    def test_find_start(self):
        data = graph.load_from_txt('../maze_03.txt')
        ans1, ans2 = graph.find_start_node(dict(), data.matrix)
        actual = [
            ans1,
            ans2.parent_node.vec,
            ans2.point.vec,
            len(ans2.neighbours),
            ans2.id,
            ans2.is_simple
        ]
        expected = [
            {(1, 0): 0},
            (None, None),
            (1, 0),
            3,
            0,
            True
        ]

        self.assertEqual(expected, actual)
