#!/home/andrey/MLNI/iu4-2k21-mlni/mironov_aa_iu4_83/env/bin/python
import sys
from typing import Union

from constants import *
from csv_utils import make_csv_matrix, get_matrix
from dkstr import find_path
from neighbours import find_paths, path_from_node
from utils import maze_is_point_node, maze_contains, Nodes, Matrix, Paths, \
    Adjacency, next_node_id, print_results, maze_cols, maze_rows, rangend, maze_is_point_end, maze_is_point_start, \
    Point, maze_is_point_wall, maze_get_cell, point_add, point_sub


def get_cell_type(nodes: Nodes, matrix: Matrix, point: Point) -> Union[NODE, PATH, EMPTY]:
    """Check if a cell is a node or a path or just a wall"""

    if maze_is_point_wall(matrix, point):
        return EMPTY

    paths = 0

    for other in (point_sub(point, side) for side in SIDES):
        # CR: and is lazy in python
        paths += maze_contains(matrix, other) and maze_is_point_node(nodes, point, maze_get_cell(matrix, other))

    if paths in [1, 3, 4]:
        return NODE

    if paths == 2:
        return PATH

    return EMPTY


def scan_maze(maze: Matrix, adj_dict: Adjacency, paths: Paths, nodes: Nodes):
    for point in rangend(maze_rows(maze), maze_cols(maze)):

        if maze_is_point_start(maze, point) or maze_is_point_end(maze, point):
            nodes[point] = next_node_id(nodes)
            find_paths(adj_dict, paths, nodes, maze, point)
        else:
            cell = get_cell_type(nodes, maze, point)

            if cell == NODE:
                nodes[point] = next_node_id(nodes)
                find_paths(adj_dict, paths, nodes, maze, point)
            elif cell == PATH:
                path_from_node(adj_dict, nodes, maze, paths, point)
            elif cell == EMPTY:
                pass


def main(path_to_file):
    maze: Matrix = get_matrix(filename=path_to_file)

    adj_dict: Adjacency = {}
    paths: Paths = {}
    nodes: Nodes = {}

    scan_maze(maze, adj_dict, paths, nodes)

    print_results(nodes, paths, adj_dict)

    make_csv_matrix(adj_dict, nodes_num=max(nodes.values()) + 1)


if __name__ == '__main__':
    path = sys.argv[1]
    import time
    start = time.time()
    main(path)
    end = time.time()
    print(f'Time: {(end - start) * 1000} ms')
    p, l = find_path()
    print(f'Minimal path: {p}, Length: {l}')
