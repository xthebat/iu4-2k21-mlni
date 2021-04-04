import itertools
from typing import Iterator, List, Optional, Dict, Tuple

from frozendict import frozendict
from annotations import Matrix, Point, HashId, PathFrom
from constants import WALL, NODE, PATH
from utils import neighbours, benchmark, replace_hash


class Maze:
    def __init__(self, matrix: Matrix):
        self._maze = matrix
        self.nodes = Nodes()
        self.paths = Paths()
        self.adjacency = Adjacency()
        self.analyzed_maze = self.scan_maze()

    def __contains__(self, point: Point):
        rows, cols = self.shape
        return 0 <= point.r < rows and 0 <= point.c < cols

    def __str__(self):
        return f'Maze({self._maze})'

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, point: Point):
        return self._maze[point.r][point.c]

    @property
    def shape(self):
        return len(self._maze), len(self._maze[0])

    @property
    def indices(self) -> Iterator[Point]:
        return [Point(point[0], point[1]) for point in itertools.product(*(range(it) for it in self.shape))]

    @staticmethod
    def point_is_start(point: Point):
        return point == (0, 0)

    def point_is_end(self, point: Point):
        return point == tuple(map(lambda x: x - 1, self.shape))

    @benchmark
    def scan_maze(self):
        rows, cols = self.shape
        analyzed_maze: List[List[Optional[Cell]]] = [[None] * cols for _ in range(rows)]

        for point in self.indices:
            curr_cell = Cell(point, self)
            analyzed_maze[point.r][point.c] = curr_cell

            if curr_cell.type == NODE:
                self.nodes.add(point)
                self.nodes.find_paths(point, self)

            if curr_cell.type == PATH:
                self.paths.add(point, self)

        return analyzed_maze


class Cell:
    def __init__(self, point: Point, maze: Maze):
        self.value = maze[point]
        self.point = point
        self.type: [NODE, WALL, PATH] = self.get_type(maze)

    def __str__(self):
        view = {
            NODE: '*',
            WALL: ' ',
            PATH: '•'
        }
        return f'{view[self.type]}'

    def __repr__(self):
        return str(self)

    def is_wall(self):
        return not self.value

    def get_type(self, maze: Maze):
        """Check if a cell is a node or a path or just a wall"""

        if maze.point_is_start(self.point) or maze.point_is_end(self.point):
            return NODE

        if self.is_wall():
            return WALL

        paths = len(list(neighbours(self.point, maze)))

        if paths in [1, 3, 4]:
            return NODE

        if paths == 2:
            return PATH

        return WALL


class Nodes(dict):
    """ Nodes contains point as key and node_id as value
        Point(r, c): node_id"""

    def next_node_id(self):
        return max(self.values()) + 1 if len(self) else 0

    def add(self, point):
        self[point] = self.next_node_id()

    def find_paths(self, point: Point, maze: Maze):
        """ Check neighbours of node cell to find paths to other nodes """
        for n_point, side in neighbours(point, maze, invert=True):

            if n_point in self:
                # Neighbour is node -> path length = 1
                maze.adjacency[(self[n_point], self[point])] = 1

            if n_point in maze.paths:
                if maze.paths.source_is_hash(n_point):            # Neighbor is not a path to the node
                    replace_hash(self[point], side, maze.paths, maze.paths[n_point])
                    if maze.paths[n_point].node_id == self[point]:
                        continue

                path_node = maze.paths[n_point].node_id
                link = (path_node, self[point])
                length = maze.paths.get_length(maze.paths[n_point])

                if link not in maze.adjacency:
                    # The neighboring cell is exactly the path to the node
                    maze.adjacency[link] = length

                elif maze.adjacency[link] > length:
                    # There are two paths to one node -> choose the shortest path
                    maze.adjacency[link] = length


class Adjacency:
    """ Adjacency contains link between nodes as key and length of path as value
        (node_id, node_id): length"""

    def __init__(self):
        self.__internals = dict()  # type: Dict[Point, int]

    def __getitem__(self, link):
        return self.__internals[link]

    def __setitem__(self, link, dist):
        self.__internals[link] = dist

    def __contains__(self, link):
        return link in self.__internals

    def links(self):
        return self.__internals.keys()

    def to_array(self) -> Matrix:
        nodes_num = max(node for link in self.links() for node in link)
        real_matrix = [[0] * nodes_num for _ in range(nodes_num)]
        for x, y in self.links():
            real_matrix[x][y] = self[x, y]
            real_matrix[y][x] = self[x, y]
        return real_matrix

    def to_dict(self):
        return frozendict(self.__internals)


class Paths(dict):
    """ Paths contains point as key and PathFrom or HashId as value
        Point(r, c): PathFrom(node_id, side) | HashId"""

    def add(self, point: Point, maze: Maze):
        self.identify_source(point, maze)

    def source_is_hash(self, point):
        return isinstance(self[point], HashId)

    def has_point_side(self, point):
        return point in self and isinstance(self[point], PathFrom)

    def get_length(self, source):
        return len([k for k, v in self.items() if v == source]) + 1

    def identify_source(self, point: Point, maze: Maze):
        """ Check neighbours of path cell to find node membership """
        for n_point, side in neighbours(point, maze):

            if n_point in maze.nodes:       # Neighbour is node
                self[point] = PathFrom(node_id=maze.nodes[n_point], side=side)

            elif n_point in self:           # Neighbour is path

                if self.has_point_side(point) and self.source_is_hash(n_point):
                    node_id, node_side = self[point].node_id, self[point].side
                    replace_hash(node_id, node_side, self, self[n_point])

                elif self.has_point_side(point) and not self.source_is_hash(n_point):
                    link = (self[point].node_id, self[n_point].node_id)
                    length = self.get_length(self[point]) + self.get_length(self[n_point]) - 1
                    maze.adjacency[link] = length

                else:
                    self[point] = self[n_point]

            elif point not in self:          # Current cell is not path
                self[point] = hash(point)

