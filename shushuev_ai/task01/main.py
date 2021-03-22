import sys
import numpy as np
from typing import List, Tuple, Dict, Union


numeric = Union[float, int]


def read_maze_from_file(filepath: str) -> List[List[int]]:
    with open(filepath, "rt") as file:
        return [[int(num) for num in line.split(' ')] for line in file]


def neighbours(maze, node):
    for drow, dcol in (0, 1), (1, 0), (0, -1), (-1, 0):
        neighbour_row, neighbour_col = node
        neighbour_row += drow
        neighbour_col += dcol
        if 0 <= neighbour_row < len(maze) and 0 <= neighbour_col < len(maze[neighbour_row]):
            yield neighbour_row, neighbour_col


def adj_from_maze(maze: List[List[int]],
                  weight_map: List[List[numeric]],
                  visited: Dict[Tuple[int, int], bool],
                  queue: List[Tuple[Tuple[int, int], Tuple[int, int]]],
                  end: Tuple[int, int],
                  adj: Dict[Tuple[int, int], Dict[Tuple[int, int], numeric]]
                  ) -> Dict[Tuple[int, int], Dict[Tuple[int, int], numeric]]:
    for root, node in queue:
        visited[node] = True
        unvisited = list(filter(lambda x: not visited.get(x, False) and maze[x[0]][x[1]] == 1, neighbours(maze, node)))

        if (len(unvisited) != 1 or node == end) and node != root:
            # получаем вес ребра
            length = weight_map[node[0]][node[1]] - weight_map[root[0]][root[1]]
            if adj.get(root) is None:
                adj[root] = {node: length}
            else:
                adj[root][node] = length

            root = node

        for neighbour in unvisited:
            row, col = neighbour
            queue.append((root, neighbour))
            weight_map[row][col] = weight_map[node[0]][node[1]] + 1

    return adj


def build_graph_from_maze_map(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int], wall=False):

    if wall:
        min_length = np.inf
        min_adj = dict()

        # do some magic
        for new_maze, weight_map, visited, queue, adj in gen_break_wall_points(maze, start, end):
            adj = adj_from_maze(new_maze, weight_map, visited, queue, end, adj)
            if weight_map[end[0]][end[1]] < min_length:
                min_length = weight_map[end[0]][end[1]]
                min_adj = adj

        return min_adj
    else:
        # в очереди хранятся пары корень, текущий узел
        queue = [(start, start)]
        weight_map = [[np.inf for _ in row] for row in maze]
        weight_map[start[0]][start[1]] = 0
        visited = dict()
        adj = dict()

        return adj_from_maze(maze, weight_map, visited, queue, end, adj)


def gen_break_wall_points(maze: List[List[int]],
                          start: Tuple[int, int],
                          end: Tuple[int, int]):
    queue = [(start, start)]
    weight_map = [[np.inf for _ in row] for row in maze]
    weight_map[start[0]][start[1]] = 0
    visited = dict()
    adj = dict()

    for i, node_chunk in enumerate(queue):
        root, node = node_chunk

        visited[node] = True
        neighs = list(neighbours(maze, node))
        unvisited = list(filter(lambda x: not visited.get(x, False) and maze[x[0]][x[1]] == 1, neighs))

        # стены у которых есть непосещенные клетки с 1
        walls = filter(
            lambda x: any(map(lambda y: not visited.get(y, False) and maze[y[0]][y[1]], neighbours(maze, x))),
            filter(lambda x: maze[x[0]][x[1]] == 0, neighs)
        )

        for wall in walls:
            q = queue[i:].copy()

            new_maze = [row.copy() for row in maze]
            new_maze[wall[0]][wall[1]] = 1

            yield new_maze, [row.copy() for row in weight_map], visited.copy(), q, {k: v.copy() for k, v in adj.items()}

        if (len(unvisited) != 1 or node == end) and node != root:
            # получаем вес ребра
            length = weight_map[node[0]][node[1]] - weight_map[root[0]][root[1]]
            if adj.get(root) is None:
                adj[root] = {node: length}
            else:
                adj[root][node] = length

            root = node

        for neighbour in unvisited:
            row, col = neighbour
            queue.append((root, neighbour))
            weight_map[row][col] = weight_map[node[0]][node[1]] + 1


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
