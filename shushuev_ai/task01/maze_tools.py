import collections
from typing import List, Union, Iterable

Numeric = Union[int, float, complex]
_matrix = List[List[Numeric]]


class Point(collections.namedtuple('base_point', 'row col')):
    def __new__(cls, row: int, col: int):
        return super(Point, cls).__new__(cls, row, col)

    def __add__(self, other):
        return Point(row=self.row + other[0], col=self.col + other[1])

    def __sub__(self, other):
        return Point(row=self.row - other[0], col=self.col - other[1])


class Maze(object):
    def __init__(self, maze_map: _matrix):
        self.maze_map = maze_map

    def __getitem__(self, p: Point) -> Numeric:
        return self.maze_map[p.row][p.col]

    def __setitem__(self, p: Point, value: Numeric):
        self.maze_map[p.row][p.col] = value

    def rows(self) -> int:
        """ Возвращает количество строк в лабиринте """
        return len(self.maze_map)

    def cols(self) -> int:
        """ Возвращает количество столбцов в лабиринте """
        return len(self.maze_map[0])

    def is_valid_point(self, p: Point) -> bool:
        """ Проверяет точку на валидность """
        return 0 <= p.row < self.rows() and 0 <= p.col < self.cols()

    def copy(self):
        """ Копирует себя """
        return Maze([[value for value in row] for row in self.maze_map])


def from_file(filepath: str) -> Maze:
    """ Читает из файла лабиринт """
    return Maze(_read_matrix_from_file(filepath))


def from_value(rows: int, cols: int, value: Numeric):
    """ Создает лабиринт размером rows x cols и заполняет все ячейки
        значением value """
    return Maze([[value for _ in range(cols)] for _ in range(rows)])


def neighbours(maze: Maze, point: Point) -> Iterable[Point]:
    """ Возвращает соседей точки point в лабиринте maze """
    for delta in (0, 1), (1, 0), (0, -1), (-1, 0):
        neigh = point + delta
        if maze.is_valid_point(neigh):
            yield neigh


def _read_matrix_from_file(filepath: str) -> _matrix:
    with open(filepath, "rt") as file:
        return [[int(num) for num in line.split(' ')] for line in file]
