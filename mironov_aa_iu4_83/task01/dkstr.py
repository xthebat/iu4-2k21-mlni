#!/home/andrey/MLNI/iu4-2k21-mlni/mironov_aa_iu4_83/env/bin/python
from csv_utils import get_matrix
from typing import Tuple

Path = Tuple[int, ...]


def indices(m):
    for y in range(m):
        for x in range(y + 1, m):
            yield y, x


def get_min_path(paths, current_node) -> Path:
    paths_to_current_node = {path: length for path, length in paths.items() if path[-1] == current_node}
    min_path = sorted(paths_to_current_node.items(), key=lambda x: x[1])
    return min_path[0][0] if min_path else ()


def find_path() -> (Path, int):
    adj_matrix = get_matrix(filename='adj.csv')

    paths = {}

    for y, x in indices(len(adj_matrix)):
        if adj_matrix[y][x]:
            min_path = get_min_path(paths, y)
            if not min_path:
                paths[(y, x)] = adj_matrix[y][x]
            else:
                min_length = paths[min_path]
                paths[(min_path + (x, ))] = adj_matrix[y][x] + min_length

    global_min_paths = get_min_path(paths, len(adj_matrix) - 1)
    return global_min_paths, paths[global_min_paths]


if __name__ == '__main__':
    p, l = find_path()
    print(f'Minimal path: {p}, Length: {l}')
