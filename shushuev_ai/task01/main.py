import sys
import numpy as np
from typing import List, Tuple


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


def build_graph_from_maze_map(maze: List[List[int]], start: Tuple[int, int], end: Tuple[int, int]):
    # в очереди хранятся пары корень, текущий узел
    queue = [(start, start)]
    weight_map = [[np.nan for _ in row] for row in maze]
    weight_map[start[0]][start[1]] = 0
    visited = dict()
    adj = dict()

    for root, node in queue:
        visited[node] = True
        unvisited = list(filter(lambda x: True if visited.get(x) is None and maze[x[0]][x[1]] == 1 else False,
                                neighbours(maze, node)))

        if len(unvisited) != 1 or node == end:
            # получаем вес ребра
            length = weight_map[node[0]][node[1]] - weight_map[root[0]][root[1]]
            if adj.get(root) is None:
                adj[root] = {node: length}
            else:
                adj[root][node] = length

            root = node

        for neighbour in unvisited:
            row, col = neighbour
            if maze[row][col] == 1:
                queue.append((root, neighbour))
                weight_map[row][col] = weight_map[node[0]][node[1]] + 1

    return adj


def main(args):
    if len(args) != 2:
        print("expected a path to maze file as first argument")
        exit(-1)

    filename = args[1]

    maze = read_maze_from_file(filename)

    adj = build_graph_from_maze_map(maze, (0, 0), (len(maze) - 1, len(maze[-1]) - 1))

    print(adj)


if __name__ == '__main__':
    main(sys.argv)
