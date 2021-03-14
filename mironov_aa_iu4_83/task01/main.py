import csv
from collections import defaultdict

from constants import *


def get_corrections(side, invert=False):
    if side == 'left':
        corr_x, corr_y = (1, 0) if not invert else (-1, 0)
    elif side == 'right':
        corr_x, corr_y = (-1, 0) if not invert else (1, 0)
    elif side == 'up':
        corr_x, corr_y = (0, 1) if not invert else (0, -1)
    elif side == 'down':
        corr_x, corr_y = (0, -1) if not invert else (0, 1)
    else:
        corr_x, corr_y = 0, 0

    return corr_x, corr_y


def get_matrix(filename):
    with open(filename, 'rt') as file:
        str_matrix = list(csv.reader(file))

    return [list(map(lambda x: int(x), str_matrix[i])) for i in range(len(str_matrix))]


def check_node(nodes, cell, x, y):
    if cell:
        if (x, y) not in nodes.values():
            return True
    return False


def check_cell(nodes, matrix, x, y):
    paths = 0
    if not matrix[y][x]:
        return EMPTY

    try:
        if check_node(nodes, matrix[y][x + 1], x, y):                   # Right
            paths += 1
    except IndexError:
        pass
    try:
        if check_node(nodes, matrix[y][x - 1], x, y) and x - 1 >= 0:    # Left
            paths += 1
    except IndexError:
        pass
    try:
        if check_node(nodes, matrix[y + 1][x], x, y):                   # Down
            paths += 1
    except IndexError:
        pass
    try:
        if check_node(nodes, matrix[y - 1][x], x, y) and y - 1 >= 0:    # Up
            paths += 1
    except IndexError:
        pass

    if paths in [1, 3, 4]:
        return NODE

    if paths == 2:
        return PATH

    return EMPTY


def path_from_node(nodes, matrix, paths, x, y):
    for side in ['left', 'right', 'up', 'down']:
        corr_x, corr_y = get_corrections(side)

        try:
            if matrix[y + corr_y][x + corr_x] and x + corr_x >= 0 and y + corr_y >= 0:
                if (x + corr_x, y + corr_y) in nodes.keys():
                    paths.update({(x, y): f'{nodes[(x + corr_x, y + corr_y)]}_{side}'})
                elif (x + corr_x, y + corr_y) in paths.keys():
                    paths.update({(x, y): paths[(x + corr_x, y + corr_y)]})
                elif (x, y) not in paths.keys():
                    paths.update({(x, y): hash((x, y))})
        except IndexError:
            pass


def get_path_length(paths, start_node):
    return len([k for k, v in paths.items() if v == start_node]) + 1


def make_path(side, node, paths, hash_value):
    new_source = f'{node}_{side}'

    for path, source in paths.items():
        if source == hash_value:
            paths[path] = new_source
        else:
            paths[path] = source


def find_paths(adj_matrix, paths, nodes, matrix, x, y):
    for side in ['left', 'right', 'up', 'down']:
        corr_x, corr_y = get_corrections(side, invert=True)
        try:
            if matrix[y + corr_y][x + corr_x]:
                if (x + corr_x, y + corr_y) in nodes.keys():
                    adj_matrix.update({
                        (nodes[(x + corr_x, y + corr_y)], nodes[(x, y)]): 1
                    })
                if (x + corr_x, y + corr_y) in paths.keys():
                    if isinstance(paths[(x + corr_x, y + corr_y)], int):
                        make_path(side, nodes[(x, y)], paths, paths[(x + corr_x, y + corr_y)])
                        if int(paths[(x + corr_x, y + corr_y)][0]) == nodes[(x, y)]:
                            continue
                    if (int(paths[(x + corr_x, y + corr_y)][0]), nodes[(x, y)]) not in adj_matrix.keys():
                        adj_matrix.update({
                            (
                                int(paths[(x + corr_x, y + corr_y)][0]),
                                nodes[(x, y)]
                            ): get_path_length(paths, paths[(x + corr_x, y + corr_y)])
                        })
                    else:
                        if adj_matrix[(
                                int(paths[(x + corr_x, y + corr_y)][0]),
                                nodes[(x, y)]
                        )] > get_path_length(paths, paths[(x + corr_x, y + corr_y)]):
                            adj_matrix.update({
                                (
                                    int(paths[(x + corr_x, y + corr_y)][0]),
                                    nodes[(x, y)]
                                ): get_path_length(paths, paths[(x + corr_x, y + corr_y)])
                            })
        except IndexError:
            pass


def csv_adj_matrix(adj, nodes_num):
    real_matrix = [[0] * nodes_num for _ in range(nodes_num)]
    for x, y in adj.keys():
        real_matrix[x][y] = adj[(x, y)]
        real_matrix[y][x] = adj[(x, y)]
    with open('adj.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(real_matrix)


def main():
    matrix = get_matrix(filename='6x5.csv')

    adj_matrix = {}
    paths = {}
    nodes = {}
    node_counter = 0

    for y, row in enumerate(matrix):
        for x, col in enumerate(row):

            if (x, y) == (0, 0) or (x, y) == (len(row) - 1, len(matrix) - 1):   # Check start and end position
                nodes.update({(x, y): node_counter})
                node_counter += 1

                find_paths(adj_matrix, paths, nodes, matrix, x, y)
                continue

            cell = check_cell(nodes, matrix, x, y)

            if cell == EMPTY:
                continue

            if cell == NODE:
                nodes.update({(x, y): node_counter})
                node_counter += 1

                find_paths(adj_matrix, paths, nodes, matrix, x, y)
                continue

            if cell == PATH:
                path_from_node(nodes, matrix, paths, x, y)
                continue

    print(f'Nodes: {nodes}')
    print(f'Paths: {paths}')

    print(f'Adj matrix: {adj_matrix}')

    csv_adj_matrix(adj_matrix, node_counter)


if __name__ == '__main__':
    main()
