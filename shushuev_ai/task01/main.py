import sys
import numpy as np
from typing import Tuple, Dict, Set
from maze_tools import Maze, Point, Numeric
import maze_tools
from li import State

Link = Tuple[Point, Point]


def adj_add_link(adj: Dict[Point, Dict[Point, Numeric]], root, node, length):
    if adj.get(root) is None:
        adj[root] = {node: length}
    else:
        adj[root][node] = length


def adj_from_maze(
        s: State,
) -> Dict[Point, Dict[Point, Numeric]]:
    for _ in s:
        pass
    return s.adj


def build_graph_from_maze(maze: Maze, start: Point, end: Point):
    s = State(maze=maze, start=start, end=end)
    return adj_from_maze(s)


def build_graph_form_maze_with_break_wall(maze: Maze, start: Point, end: Point):
    min_length = np.inf
    min_adj = dict()

    # do some magic
    for state in gen_break_wall_points(maze, start, end):
        adj = adj_from_maze(state)
        if state.weight_map[end] < min_length:
            min_length = state.weight_map[end]
            min_adj = adj

    return min_adj


def neighs_has_pass(maze: Maze, visited: Set[Point], point: Point):
    return any(map(lambda it: it not in visited and maze[it], maze_tools.neighbours(maze, point)))


def neighs_get_passes(maze: Maze, visited: Set[Point], point: Point):
    return set(filter(lambda it: it not in visited and maze[it], maze_tools.neighbours(maze, point)))


def neighs_get_walls(maze: Maze, point: Point):
    return filter(lambda x: not maze[x], maze_tools.neighbours(maze, point))


def gen_break_wall_points(maze: Maze, start: Point, end: Point):
    state = State(maze=maze, end=end, start=start)
    for node in state:

        walls = filter(lambda w: neighs_has_pass(state.maze, state.visited, w), neighs_get_walls(state.maze, node))

        for wall in walls:
            new_state = state.copy()
            new_state.maze[wall] = 1

            yield new_state


def main(args):
    if len(args) != 2:
        print("expected a path to maze file as first argument")
        exit(-1)

    filename = args[1]

    maze = maze_tools.from_file(filename)

    adj = build_graph_from_maze(maze, Point(row=0, col=0), Point(row=maze.rows() - 1, col=maze.cols() - 1))

    print(adj)


if __name__ == '__main__':
    main(sys.argv)
