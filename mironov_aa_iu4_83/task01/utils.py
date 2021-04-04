import itertools
from typing import Iterator

from annotations import Point, PathFrom
from constants import SIDES, LEFT, RIGHT, UP, DOWN


def ranged(*args: int) -> Iterator[Point]:
    return itertools.product(*(range(it) for it in args))


def replace_hash(node: int, side: SIDES, paths, hash_value: int) -> None:
    """ Replace hash with a PathFrom """
    new_source = PathFrom(node_id=node, side=side)

    for path, source in paths.items():
        paths[path] = new_source if source == hash_value else source


_corrections = {
    LEFT: Point(0, 1),
    RIGHT: Point(0, -1),
    UP: Point(1, 0),
    DOWN: Point(-1, 0)
}

_invert_corrections = {
    RIGHT: Point(0, 1),
    LEFT: Point(0, -1),
    DOWN: Point(1, 0),
    UP: Point(-1, 0)
}


def print_results(maze):
    print(f'Nodes: {maze.nodes}')

    print(f'Adjacency dict: {maze.adjacency}')

    print('Pretty maze:')

    for i in maze.analyzed_maze:
        print(*i)


def neighbours(point, maze, invert=False):
    """ Returns point of available neighbours """
    for side in SIDES:
        corr = _corrections[side] if not invert else _invert_corrections[side]

        n_point = Point(point.r + corr.r, point.c + corr.c)

        if n_point in maze and maze[n_point]:
            yield n_point, side


def benchmark(func):
    """ Check time of function executing """
    import time

    def wrapper(*args, **kwargs):
        start = time.time()

        return_value = func(*args, **kwargs)

        end = time.time()
        print(f'Time for {func.__name__}: {(end - start) * 1000} ms')
        return return_value

    return wrapper
