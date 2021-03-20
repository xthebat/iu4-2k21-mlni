#!/home/andrey/MLNI/iu4-2k21-mlni/mironov_aa_iu4_83/env/bin/python

from typing import Union

from constants import *
from csv_utils import make_csv_matrix, get_matrix
from neighbours import find_paths, path_from_node
from utils import start_or_end_position, check_node, pointer_in_maze_scope, Nodes, Matrix, Paths, \
    Adj_dict, next_node_id, print_results, get_corrections


def check_cell(nodes: Nodes, matrix: Matrix, x: int, y: int) -> Union[NODE, PATH, EMPTY]:
    """ Check if a cell is a node or a path or empty """
    paths = 0
    if not matrix[y][x]:
        return EMPTY

    for side in SIDES:
        corr_x, corr_y = get_corrections(side, invert=True)
        if pointer_in_maze_scope(x + corr_x, y + corr_y, matrix):
            if check_node(nodes, matrix[y + corr_y][x + corr_x], x, y):
                paths += 1

    if paths in [1, 3, 4]:
        return NODE

    if paths == 2:
        return PATH

    return EMPTY


def scan_maze(maze: Matrix, adj_dict: Adj_dict, paths: Paths, nodes: Nodes):
    for y, row in enumerate(maze):
        for x, col in enumerate(row):

            if start_or_end_position(x, y, len(row), len(maze)):
                nodes.update({(x, y): next_node_id(nodes)})
                find_paths(adj_dict, paths, nodes, maze, x, y)
                continue

            cell = check_cell(nodes, maze, x, y)

            if cell == EMPTY:
                continue

            if cell == NODE:
                nodes.update({(x, y): next_node_id(nodes)})

                find_paths(adj_dict, paths, nodes, maze, x, y)
                continue

            if cell == PATH:
                path_from_node(nodes, maze, paths, x, y)
                continue


def main():
    maze: Matrix = get_matrix(filename='6x5.csv')

    adj_dict: Adj_dict = {}
    paths: Paths = {}
    nodes: Nodes = {}

    scan_maze(maze, adj_dict, paths, nodes)

    print_results(nodes, paths, adj_dict)

    make_csv_matrix(adj_dict, nodes_num=max(nodes.values()) + 1)


if __name__ == '__main__':
    import time
    start = time.time()
    main()
    end = time.time()
    print(f'Time: {(end - start) * 1000} ms')
