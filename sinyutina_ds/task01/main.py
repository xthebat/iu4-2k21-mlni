import sys
from typing import List, IO, Tuple, Dict, Iterable, Generator

Point = Tuple[int, int]
Adj = Dict[Point, Dict[Point, int]]
Map = List[List[int]]


def parse_maze_map(file: IO) -> Map:
    return [[int(x) for x in line.split(', ')] for line in file]


def read_maze_map(path: str) -> Map:
    with open(path) as file:
        return parse_maze_map(file)


def adj_add_link(adj: Adj, prev: Point, node: Point, weight: int):
    if adj.get(prev) is None:
        adj[prev] = {node: weight}
    else:
        adj[prev][node] = weight

    if adj.get(node) is None:
        adj[node] = {prev: weight}
    else:
        adj[node][prev] = weight


def make_maze_graph(maze_map: Map) -> Adj:
    # Функция обходит построчно таблицу. Поскольку для построения неоптимизированной матрицы смежности
    # нам не нужна информация об сосдених ячейках на следующей или текущей строки (мы и так их посетим)
    # построение графа исходит из занесения в матрицу смежности узла по предшествующему узлу.
    adj = dict()
    for i, row in enumerate(maze_map):
        prev = 0  # prev нужен для того чтобы не проверять j на 0 и хранить значение предыдущей в строке ячейки
        for j, val in enumerate(row):
            if val == 1:
                curr_vertex_id = (i, j)

                if prev == 1:
                    prev_vertex_id = (i, j - 1)

                    adj_add_link(adj, curr_vertex_id, prev_vertex_id, 1)

                if i > 0 and maze_map[i - 1][j] == 1:
                    prev_vertex_id = (i - 1, j)

                    adj_add_link(adj, curr_vertex_id, prev_vertex_id, 1)

            prev = val
    return adj


def simplify_paths(adj: Adj, start: Point, end: Point) -> Adj:
    nodes_queue = [(start, start, 0)]  # в queue содержится (предудщий узел, текущая вершина, вес простого пути)
    # предыдущий узел start для случая когда стартовый узел имеет число соседей == 1

    visited = set()
    new_adj = dict()
    # Обходим по всем элементам в очереди
    for prev, curr, weight in nodes_queue:
        visited.add(curr)

        # получаем список непосещенных соседей
        neighbors = list(filter(lambda kv: kv[0] not in visited, adj[curr].items()))

        # Сравнение по end исключает ситуацию, когда end - промежуточная вершина в простом пути
        if len(neighbors) != 1 or curr == end:
            if prev != curr:
                adj_add_link(new_adj, prev, curr, weight)

            weight = 0
            prev = curr

        for k, v in neighbors:
            nodes_queue.append((prev, k, weight + v))

    return new_adj


def gen_min_weight(queue: Dict[Tuple[Point, Point], int]) -> Generator[Tuple[Point, Point, int], None, None]:
    while len(queue):
        k = min(queue, key=lambda x: queue[x])
        w = queue[k]
        queue.pop(k)
        yield *k, w


def restore_path(prev_nodes: Dict[Point, Point], start: Point, end: Point) -> List[Point]:
    path = []
    if end in prev_nodes:
        while end != start:
            path.insert(0, end)
            end = prev_nodes[end]

        path.insert(0, start)

    return path


def find_path(adj: Adj, start: Point, end: Point) -> List[Point]:
    prev_nodes = dict()
    queue = {(None, start): 0}
    visited = set()

    for prev, node, weight in gen_min_weight(queue):
        visited.add(node)

        for neigh in filter(lambda x: x not in visited, adj[node]):
            queue[(node, neigh)] = weight + adj[node][neigh]

        if prev is not None:
            prev_nodes[node] = prev

    return restore_path(prev_nodes, start, end)


def main(args):
    if len(args) != 2:
        print("В аргументах ожидается путь до файла с лабиринтом")
        exit(-1)

    path = args[1]

    maze_map = read_maze_map(path)

    adj = make_maze_graph(maze_map)

    adj = simplify_paths(adj, (0, 0), (len(maze_map) - 1, len(maze_map[-1]) - 1))

    path = find_path(adj, (0, 0), (len(maze_map) - 1, len(maze_map[-1]) - 1))

    print(path)


if __name__ == '__main__':
    main(sys.argv)
