import sys
from typing import List, Dict


def parse_maze_map(file) -> List[List[int]]:
    return [[int(x) for x in line.split(', ')] for line in file]


def read_maze_map(path: str) -> List[List[int]]:
    with open(path) as file:
        return parse_maze_map(file)


def make_maze_graph(maze_map: List[List[int]]) -> Dict[str, Dict[str, int]]:
    prev = 0
    vertex_id = 1

    adj = dict()
    vertex_map = [['' for i in range(len(row))] for row in maze_map]

    for i in range(len(maze_map[0])):
        if maze_map[0][i] == 1:
            curr_vertex_id = str(vertex_id)
            vertex_map[0][i] = curr_vertex_id
            adj[curr_vertex_id] = dict()

            if prev == 1:
                prev_vertex_id = vertex_map[0][i - 1]
                adj[curr_vertex_id][prev_vertex_id] = 1
                adj[prev_vertex_id][curr_vertex_id] = 1

            vertex_id += 1

        prev = maze_map[0][i]

    for i in range(1, len(maze_map)):
        prev = 0
        for j in range(len(maze_map[i])):
            if maze_map[i][j] == 1:
                curr_vertex_id = str(vertex_id)
                vertex_map[i][j] = curr_vertex_id
                adj[curr_vertex_id] = dict()

                if prev == 1:
                    prev_vertex_id = vertex_map[i][j - 1]

                    adj[curr_vertex_id][prev_vertex_id] = 1
                    adj[prev_vertex_id][curr_vertex_id] = 1

                if maze_map[i - 1][j] == 1:
                    prev_vertex_id = vertex_map[i - 1][j]

                    adj[curr_vertex_id][prev_vertex_id] = 1
                    adj[prev_vertex_id][curr_vertex_id] = 1

                vertex_id += 1

            prev = maze_map[i][j]

    return adj


def main(args):
    if len(args) < 2:
        print("введите путь до файла c лабиринтом: ")
        path = input()
    elif len(args) > 3:
        print("слишком много аргументов, введите название файла: ")
        path = input()
    else:
        path = args[1]

    maze_map = read_maze_map(path)

    adj = make_maze_graph(maze_map)

    print(maze_map)
    print(adj)


if __name__ == '__main__':
    main(sys.argv)
