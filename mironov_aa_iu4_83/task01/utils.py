import itertools
from collections import defaultdict
from pprint import pprint
from typing import List, Dict, Tuple, Union, Iterator

from constants import SIDES, LEFT, RIGHT, UP, DOWN

Matrix = List[List[int]]
Nodes = Dict[Tuple[int, int], int]
Paths = Dict[Tuple[int, int], Union[str, int]]
Adjacency = Dict[Tuple[int, int], int]
Point = Tuple[int, int]


def rangend(*args: int) -> Iterator:
    return itertools.product(*(range(it) for it in args))


def node_side_from_point(nodes: Nodes, point: Point, side: str):
    return f'{nodes[point]}_{side}'


def node_side_from_hash(side: SIDES, node: int, paths: Paths, hash_value: int) -> None:
    """ Replace hash with a node_side """
    new_source = f'{node}_{side}'

    for path, source in paths.items():
        paths[path] = new_source if source == hash_value else source


def point_row(point: Point):
    return point[0]


def point_col(point: Point):
    return point[1]


_name2point = {
    LEFT: (1, 0),
    RIGHT: (-1, 0),
    UP: (0, 1),
    DOWN: (0, -1)
}


def point_add(point: Point, other: Union[Point, str]) -> Point:
    if isinstance(other, tuple):
        return point[0] + other[0], point[1] + other[1]
    elif isinstance(other, str):
        return point_add(point, _name2point[other])


def point_sub(point: Point, other: Union[Point, str]) -> Point:
    if isinstance(other, tuple):
        return point[0] - other[0], point[1] - other[1]
    elif isinstance(other, str):
        return point_sub(point, _name2point[other])


def maze_rows(maze: Matrix):
    return len(maze)


def maze_cols(maze: Matrix):
    return len(maze[0])


def maze_is_point_start(maze: Matrix, point: Point):
    return point == (0, 0)


def maze_is_point_end(maze: Matrix, point: Point):
    return point == (maze_rows(maze) - 1, maze_cols(maze) - 1)


def maze_is_point_node(nodes: Nodes, point: Point, cell: int) -> bool:
    if cell:
        # CR: very, very strange: nodes.values() is int's (path lengths) why we search point in length?
        if point not in nodes.values():
            return True
    return False


def maze_get_cell(maze: Matrix, point: Point):
    return maze[point[0]][point[1]]


def maze_is_point_wall(maze: Matrix, point: Point):
    return not maze_get_cell(maze, point)


def maze_contains(maze: Matrix, point: Point) -> bool:
    return 0 <= point[1] < len(maze[0]) and 0 <= point[0] < len(maze)


def next_node_id(nodes: Nodes) -> int:
    return max(nodes.values()) + 1 if len(nodes) else 0


def path_is_point_hash(paths: Paths, point: Point) -> bool:
    return isinstance(paths[point], int)


def path_get_node_id(paths: Paths, point: Point) -> int:
    return int(paths[point][0])


# CR: It's for sure better to use Namedtuple, storing information in string with '_' decimeter is weird
def path_get_point_side(paths: Paths, point: Point) -> str:
    return paths[point].split('_')[1]


def path_has_point_side(paths: Paths, point: Point):
    return point in paths and isinstance(paths[point], str)


def path_get_length(paths: Paths, start_node: str) -> int:
    return len([k for k, v in paths.items() if v == start_node]) + 1


def print_results(nodes: Nodes, paths: Paths, adj_dict: Adjacency):
    print(f'Nodes: {nodes}')

    pretty_paths = defaultdict(list)
    for k, v in paths.items():
        pretty_paths[v].append(k)

    print('Paths: ')
    pprint(dict(pretty_paths))

    print(f'Adjacency dict: {adj_dict}')
