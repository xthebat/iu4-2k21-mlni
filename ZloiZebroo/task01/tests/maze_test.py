import unittest
from task01 import maze as graph


class MazeTests(unittest.TestCase):

    def test_graph_02(self):
        data = graph.load_from_txt('../maze_02.txt')
        actual = [data.nodes, data.adj, data.adj_matrix, data.matrix.data]
        expected = [
            {0: [0, 0], 1: [9, 0], 2: [1, 2], 3: [9, 2], 4: [9, 4], 5: [9, 5]},
            {0: {2: 3},
             1: {3: 2},
             2: {0: 3, 4: 10},
             3: {1: 2, 4: 2},
             4: {2: 10, 3: 2, 5: 1},
             5: {4: 1}},
            [[None, None, 3, None, None, None],
             [None, None, None, 2, None, None],
             [3, None, None, None, 10, None],
             [None, 2, None, None, 2, None],
             [None, None, 10, 2, None, 1],
             [None, None, None, None, 1, None]],
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
            {0: [1, 0], 1: [0, 1], 2: [1, 1], 3: [2, 1], 4: [1, 2]},
            {0: {1: 2, 2: 1, 3: 2},
             1: {0: 2, 4: 2},
             2: {0: 1, 4: 1},
             3: {0: 2, 4: 2},
             4: {1: 2, 2: 1, 3: 2}},
            [[None, 2, 1, 2, None],
             [2, None, None, None, 2],
             [1, None, None, None, 1],
             [2, None, None, None, 2],
             [None, 2, 1, 2, None]]
        ]
        self.assertEqual(expected, actual)

    def test_shortest_way(self):
        data = graph.load_from_txt('../maze_07.txt')
        data = graph.shortest_way(1, 0, data, brake_wall=False)
        actual = [data.shortest_way, data.shortest_way_len]
        expected = [[1, 0], 9]
        self.assertEqual(expected, actual)

    def test_shortest_way_brake_wall(self):
        data = graph.load_from_txt('../maze_07.txt')
        data = graph.shortest_way(1, 0, data, brake_wall=True)
        actual = [data.shortest_way, data.shortest_way_len]
        expected = [[1, 4, 5, 3, 0], 7]
        self.assertEqual(expected, actual)

    def test_raycast(self):
        data = graph.load_from_txt('../maze_07.txt')
        matrix = data.matrix
        actual = [graph.ray_cast('1', (0, 0), graph.Point(0, 0), matrix),
                  graph.ray_cast('1', (1, 0), graph.Point(0, 0), matrix),
                  graph.ray_cast('1', (0, 0), graph.Point(0, 1), matrix)]
        expected = [False, False, True]
        self.assertEqual(expected, actual)

    def test_shortest_way_brake_wall_2(self):
        data = graph.load_from_txt('../maze_09.txt')
        data = graph.shortest_way(0, 3, data, brake_wall=True)
        actual = [data.shortest_way, data.shortest_way_len]
        expected = [[0, 1, 2, 4, 3], 5]
        self.assertEqual(expected, actual)
