import unittest
import main


class Tests(unittest.TestCase):
    def test_read_maze(self):
        expected = [
            [1, 1, 0, 1, 1, 1],
            [0, 1, 0, 1, 0, 0],
            [0, 1, 0, 1, 1, 1],
            [0, 1, 1, 1, 0, 1],
            [0, 1, 0, 0, 0, 1],
            [0, 1, 1, 1, 0, 1]
        ]
        received = main.read_maze_map('maze.txt')
        self.assertEqual(expected, received)

    def test_build_graph(self):
        maze = [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 1]
        ]

        expected = {
            (0, 0): {(0, 1): 1},
            (0, 1): {(0, 0): 1, (0, 2): 1, (1, 1): 1},
            (0, 2): {(0, 1): 1},
            (1, 1): {(0, 1): 1, (2, 1): 1},
            (2, 1): {(1, 1): 1, (2, 2): 1},
            (2, 2): {(2, 1): 1},
        }
        received = main.make_maze_graph(maze)
        self.assertEqual(expected, received, msg=f'expected:\n{expected}\nreceived:\n{received}')

    def test_simplify_uncycled_paths(self):
        maze = [
            [1, 1, 1],
            [0, 1, 0],
            [0, 1, 1]
        ]

        expected = {
            (0, 0): {(0, 1): 1},
            (0, 1): {(0, 0): 1, (0, 2): 1, (2, 2): 3},
            (0, 2): {(0, 1): 1},
            (2, 2): {(0, 1): 3}
        }

        received = main.simplify_paths(main.make_maze_graph(maze), (0, 0), (2, 2))

        self.assertEqual(expected, received)

    def test_simplify_cycled_paths(self):
        maze = [
            [1, 1, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 1, 1],
            [0, 0, 1, 0],
            [0, 0, 1, 1]
        ]

        expected = {
            (0, 0): {(0, 1): 1},
            (0, 1): {(0, 0): 1, (2, 2): 3, (2, 3): 4},
            (2, 2): {(0, 1): 3, (4, 3): 3, (2, 3): 1},
            (2, 3): {(0, 1): 4, (2, 2): 1},
            (4, 3): {(2, 2): 3}
        }

        received = main.simplify_paths(main.make_maze_graph(maze), (0, 0), (4, 3))
        self.assertEqual(expected, received)

    def test_simplify_paths_with_cycled_start(self):
        maze = [
            [1, 1, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 0],
            [1, 1, 1, 1],
        ]

        expected = {
            (0, 0): {(3, 3): 6, (1, 3): 4},
            (3, 3): {(0, 0): 6},
            (1, 3): {(0, 0): 4}
        }

        received = main.simplify_paths(main.make_maze_graph(maze), (0, 0), (3, 3))
        self.assertEqual(expected, received)

    def test_simplify_paths_with_cycled_end(self):
        maze = [
            [1, 0, 1, 1],
            [1, 0, 0, 1],
            [1, 0, 0, 1],
            [1, 1, 1, 1],
        ]

        expected = {
            (0, 0): {(3, 3): 6},
            (3, 3): {(0, 0): 6, (0, 2): 4},
            (0, 2): {(3, 3): 4}
        }

        received = main.simplify_paths(main.make_maze_graph(maze), (0, 0), (3, 3))
        self.assertEqual(expected, received)

    def test_find_simple_path(self):
        adj = {
            (0, 0): {(3, 3): 6},
            (3, 3): {(0, 0): 6},
        }

        expected = [(0, 0), (3, 3)]
        received = main.find_path(adj, (0, 0), (3, 3))
        self.assertEqual(expected, received)

    def test_find_path(self):
        adj = {
            (0, 0): {(0, 1): 1},
            (0, 1): {(0, 0): 1, (2, 2): 3, (2, 3): 4},
            (2, 2): {(0, 1): 3, (4, 3): 3, (2, 3): 1},
            (2, 3): {(0, 1): 4, (2, 2): 1},
            (4, 3): {(2, 2): 3}
        }

        expected = [(0, 0), (0, 1), (2, 2), (4, 3)]
        received = main.find_path(adj, (0, 0), (4, 3))
        self.assertEqual(expected, received)

    def test_find_path_in_maze_without_path(self):
        adj = {
            (0, 0): {(0, 1): 1},
            (0, 1): {(0, 0): 1},
            (2, 4): {(4, 4): 2},
            (4, 4): {(2, 4): 2}
        }
        expected = []
        received = main.find_path(adj, (0, 0), (4, 4))
        self.assertEqual(expected, received)
