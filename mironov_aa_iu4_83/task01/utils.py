from collections import defaultdict
from pprint import pprint
from typing import List, Dict, Tuple, Union

from constants import SIDES

Matrix = List[List[int]]
Nodes = Dict[Tuple[int, int], int]
Paths = Dict[Tuple[int, int], Union[str, int]]
Adj_dict = Dict[Tuple[int, int], int]


def get_corrections(side: SIDES, invert: bool = False) -> Tuple[int, int]:
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


def make_node_side_from_hash(side: SIDES, node: int, paths: Paths, hash_value: int) -> None:
    """ Replace hash with a node_side """
    new_source = f'{node}_{side}'

    for path, source in paths.items():
        paths[path] = new_source if source == hash_value else source


def start_or_end_position(x: int, y: int, row_len: int, col_len: int) -> bool:
    return (x, y) == (0, 0) or (x, y) == (row_len - 1, col_len - 1)


def get_path_length(paths: Paths, start_node) -> int:
    return len([k for k, v in paths.items() if v == start_node]) + 1


def check_node(nodes: Nodes, cell: int, x: int, y: int) -> bool:
    if cell:
        if (x, y) not in nodes.values():
            return True
    return False


def pointer_in_maze_scope(x: int, y: int, matrix: Matrix) -> bool:
    return 0 <= x < len(matrix[0]) and 0 <= y < len(matrix)


def next_node_id(nodes: Nodes) -> int:
    return max(nodes.values()) + 1 if len(nodes) else 0


def node_id_is_hash(paths: Paths, x: int, y: int) -> bool:
    return isinstance(paths[(x, y)], int)


def node_id(paths: Paths, x: int, y: int) -> int:
    return int(paths[(x, y)][0])


def cell_is_node(nodes: Nodes, x: int, y: int):
    return (x, y) in nodes.keys()


def cell_is_path(paths: Paths, x: int, y: int):
    return (x, y) in paths.keys()


def print_results(nodes: Nodes, paths: Paths, adj_dict: Adj_dict):
    print(f'Nodes: {nodes}')

    pretty_paths = defaultdict(list)
    for k, v in paths.items():
        pretty_paths[v].append(k)

    print('Paths: ')
    pprint(dict(pretty_paths))

    print(f'Adjacency dict: {adj_dict}')
