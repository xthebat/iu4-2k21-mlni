import sys
from typing import List


def parse_maze_map(file) -> List[List[int]]:
    return [[int(x) for x in line.split(', ')] for line in file]


def read_maze_map(path: str) -> List[List[int]]:
    with open(path) as file:
        return parse_maze_map(file)


def make_maze_graph(maze_map: List[List[int]]):
    # Функция обходит построчно таблицу. Поскольку для построения неоптимизированной матрицы смежности
    # нам не нужна информация об сосдених ячейках на следующей или текущей строки (мы и так их посетим)
    # построение графа исходит из занесения в матрицу смежности узла по предшествующему узлу.
    adj = dict()
    for i, row in enumerate(maze_map):
        prev = 0  # prev нужен для того чтобы не проверять j на 0 и хранить значение предыдущей в строке ячейки
        for j, val in enumerate(row):
            if val == 1:
                curr_vertex_id = (i, j)
                adj[curr_vertex_id] = dict()

                if prev == 1:
                    prev_vertex_id = (i, j - 1)

                    adj[curr_vertex_id][prev_vertex_id] = 1
                    adj[prev_vertex_id][curr_vertex_id] = 1

                if i > 0 and maze_map[i - 1][j] == 1:
                    prev_vertex_id = (i - 1, j)

                    adj[curr_vertex_id][prev_vertex_id] = 1
                    adj[prev_vertex_id][curr_vertex_id] = 1

            prev = val
    return adj


def simplify_paths(adj, start, end):
    nodes_queue = [(start, start, 0)]  # в queue содержится (предудщий узел, текущая вершина, вес простого пути)
    # предыдущий узел start для случая когда стартовый узел имеет число соседей == 1

    visited = dict()
    new_adj = dict()
    # Обходим по всем элементам в очереди
    for prev, curr, weight in nodes_queue:
        visited[curr] = True

        # получаем список непосещенных соседей
        neighbors = list(filter(lambda kv: True if visited.get(kv[0]) is None else False, adj[curr].items()))

        # Сравнение по end исключает ситуацию, когда end - промежуточная вершина в простом пути
        if len(neighbors) != 1 or curr == end:
            if prev != curr:
                if new_adj.get(prev) is None:
                    new_adj[prev] = {curr: weight}
                else:
                    new_adj[prev][curr] = weight

                if new_adj.get(curr) is None:
                    new_adj[curr] = {prev: weight}
                else:
                    new_adj[curr][prev] = weight

            weight = 0
            prev = curr

        for k, v in neighbors:
            nodes_queue.append((prev, k, weight + v))

    return new_adj


def main(args):
    if len(args) != 2:
        print("В аргументах ожидается путь до файла с лабиринтом")
        exit(-1)

    path = args[1]

    maze_map = read_maze_map(path)

    adj = make_maze_graph(maze_map)

    adj = simplify_paths(adj, (0, 0), (len(maze_map) - 1, len(maze_map[-1]) - 1))

    print(adj)


if __name__ == '__main__':
    main(sys.argv)
