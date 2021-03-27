import sys
import numpy as np
from typing import List, Tuple, Dict, Union, Set

numeric = Union[float, int]
Matrix = List[List[numeric]]
Point = Tuple[int, int]
Link = Tuple[Point, Point]


def matrix_init(rows: int, cols: int, value: numeric) -> Matrix:
    return [[value for _ in range(cols)] for _ in range(rows)]


def matrix_get(maze: Matrix, point: Point) -> int:
    return maze[point[0]][point[1]]


def matrix_set(maze: Matrix, point: Point, value: numeric):
    maze[point[0]][point[1]] = value


def matrix_rows(maze: Matrix) -> int:
    return len(maze)


def matrix_cols(maze: Matrix) -> int:
    return len(maze[0])


def neighs_has_pass(maze: Matrix, visited: Set[Point], point: Point):
    return any(map(lambda it: it not in visited and matrix_get(maze, it), neighbours(maze, point)))


def neighs_get_passes(maze: Matrix, visited: Set[Point], point: Point):
    return list(filter(lambda it: it not in visited and matrix_get(maze, it) == 1, neighbours(maze, point)))


def neighs_get_walls(maze: Matrix, point: Point):
    return filter(lambda x: not matrix_get(maze, x), neighbours(maze, point))


def read_maze_from_file(filepath: str) -> Matrix:
    with open(filepath, "rt") as file:
        return [[int(num) for num in line.split(' ')] for line in file]


def neighbours(maze, node):
    for drow, dcol in (0, 1), (1, 0), (0, -1), (-1, 0):
        neighbour_row, neighbour_col = node
        neighbour_row += drow
        neighbour_col += dcol
        if 0 <= neighbour_row < len(maze) and 0 <= neighbour_col < len(maze[neighbour_row]):
            yield neighbour_row, neighbour_col


def adj_from_maze(
        maze: Matrix,
        weight_map: Matrix,
        visited: Set[Point],
        queue: List[Link],
        end: Point,
        adj: Dict[Point, Dict[Point, numeric]]
) -> Dict[Point, Dict[Point, numeric]]:
    for root, node in queue:
        visited.add(node)
        unvisited = neighs_get_passes(maze, visited, node)

        if (len(unvisited) != 1 or node == end) and node != root:
            # получаем вес ребра
            length = matrix_get(weight_map, node) - matrix_get(weight_map, root)
            if root not in adj:
                adj[root] = {node: length}
            adj[root][node] = length

            root = node

        for neighbour in unvisited:
            queue.append((root, neighbour))
            matrix_set(weight_map, neighbour, matrix_get(weight_map, node) + 1)

    return adj


def build_graph_from_maze_map(maze: Matrix, start: Point, end: Point, wall=False):
    if wall:
        min_length = np.inf
        min_adj = dict()

        # do some magic
        for new_maze, weight_map, visited, queue, adj in gen_break_wall_points(maze, start, end):
            adj = adj_from_maze(new_maze, weight_map, visited, queue, end, adj)
            if matrix_get(weight_map, end) < min_length:
                min_length = matrix_get(weight_map, end)
                min_adj = adj

        return min_adj
    else:
        # в очереди хранятся пары корень, текущий узел
        queue = [(start, start)]
        weight_map = [[np.inf for _ in row] for row in maze]
        matrix_set(weight_map, start, 0)
        visited = set()
        adj = dict()

        return adj_from_maze(maze, weight_map, visited, queue, end, adj)


def gen_break_wall_points(maze: Matrix, start: Point, end: Point):
    queue = [(start, start)]
    weight_map = matrix_init(matrix_rows(maze), matrix_cols(maze), np.inf)
    matrix_set(weight_map, start, 0)
    visited = set()
    adj = dict()

    for i, node_chunk in enumerate(queue):
        root, node = node_chunk

        visited.add(node)
        unvisited = neighs_get_passes(maze, visited, node)

        # стены у которых есть непосещенные клетки с 1

        walls = filter(lambda wall: neighs_has_pass(maze, visited, wall), neighs_get_walls(maze, node))

        for wall in walls:
            q = queue[i:].copy()

            new_maze = [row.copy() for row in maze]
            matrix_set(new_maze, wall, 1)

            # CR: а зачем здесь копирование всего подряд? visited - локальная переменная по идее она не должна
            #     случайно поменяться
            # CR: грустно, что очень много возвращается значений через tuple и неплохо бы разделить хотя бы на
            #     отдельные переменные
            yield new_maze, [row.copy() for row in weight_map], visited.copy(), q, {k: v.copy() for k, v in adj.items()}

        if (len(unvisited) != 1 or node == end) and node != root:
            # получаем вес ребра
            length = matrix_get(weight_map, node) - matrix_get(weight_map, root)
            if root not in adj:
                adj[root] = {node: length}
            adj[root][node] = length

            root = node

        for neighbour in unvisited:
            queue.append((root, neighbour))
            matrix_set(weight_map, neighbour, matrix_get(weight_map, node) + 1)


def main(args):
    if len(args) != 2:
        print("expected a path to maze file as first argument")
        exit(-1)

    filename = args[1]

    maze = read_maze_from_file(filename)

    adj = build_graph_from_maze_map(maze, (0, 0), (len(maze) - 1, len(maze[-1]) - 1), wall=True)

    print(adj)


if __name__ == '__main__':
    main(sys.argv)
