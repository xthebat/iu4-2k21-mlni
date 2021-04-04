import unittest
import main
from task01 import maze_tools
from maze_tools import Point, Maze


class Test(unittest.TestCase):
    def test_read_maze(self):
        filename = 'test.csv'
        expected = [
            [1, 0, 0, 1],
            [1, 1, 1, 1],
            [0, 0, 1, 0],
            [1, 1, 1, 1]
        ]
        received = maze_tools._read_matrix_from_file(filename)
        self.assertEqual(expected, received)

    def test_build_graph_simple_case(self):
        maze = [
            [1, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 1, 1]
        ]

        expected = {
            (0, 0): {(3, 3): 6}
        }
        received = main.build_graph_from_maze(Maze(maze), Point(0, 0), Point(3, 3))
        self.assertEqual(expected, received)

    def test_build_graph_island_case(self):
        maze = [
            [1, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 1, 0],
            [1, 0, 1, 1]
        ]

        expected = {
            (0, 0): {(3, 3): 6}
        }
        received = main.build_graph_from_maze(Maze(maze), Point(0, 0), Point(3, 3))
        self.assertEqual(expected, received)

    def test_build_graph_mult_nodes_case(self):
        maze = [
            [1, 0, 1, 1],
            [1, 1, 1, 0],
            [1, 0, 1, 0],
            [1, 0, 1, 1]
        ]

        expected = {
            (0, 0): {(1, 0): 1},
            (1, 0): {(3, 0): 2, (1, 2): 2},
            (1, 2): {(0, 3): 2, (3, 3): 3}
        }
        received = main.build_graph_from_maze(Maze(maze), Point(0, 0), Point(3, 3))
        self.assertEqual(expected, received)

    def test_build_graph_cycled_path(self):
        maze = [
            [1, 0, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 1, 1, 1, 1]
        ]

        expected = {
            (0, 0): {(2, 0): 2},
            (2, 0): {(4, 4): 6, (2, 4): 8},
            (4, 4): {(2, 4): 2}
        }
        received = main.build_graph_from_maze(Maze(maze), Point(0, 0), Point(4, 4))
        self.assertEqual(expected, received)

    def test_build_graph_break_wall(self):
        maze = [
            [1, 0, 1, 1, 1],
            [1, 0, 1, 0, 1],
            [1, 1, 1, 0, 1],
            [1, 0, 0, 0, 1],
            [1, 0, 1, 1, 1]
        ]

        expected = {
            (0, 0): {(0, 2): 2, (2, 0): 2},
            (0, 2): {(2, 2): 2, (4, 4): 6},
            (2, 0): {(2, 2): 2, (4, 0): 2},
            (4, 4): {(4, 2): 2}
        }
        received = main.build_graph_form_maze_with_break_wall(Maze(maze), Point(0, 0), Point(4, 4))
        self.assertEqual(expected, received)

    def test_build_graph_without_path(self):
        maze = [
            [1, 0, 0],
            [0, 0, 0],
            [1, 1, 1]
        ]

        expected = {}
        received = main.build_graph_from_maze(Maze(maze), Point(0, 0), Point(2, 2))
        self.assertEqual(expected, received)

    def test_build_graph_without_path_break_wall(self):
        maze = [
            [1, 0, 0],
            [0, 0, 0],
            [1, 1, 1]
        ]

        expected = {
            (0, 0): {(2, 2): 4}
        }

        received = main.build_graph_form_maze_with_break_wall(Maze(maze), Point(0, 0), Point(2, 2))
        self.assertEqual(expected, received)
