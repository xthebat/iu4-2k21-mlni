import json
import itertools
from typing import Iterator
import math
import copy

# Пример графа, который должен получиться
# {
#   "adj": {
#     "s": { "a": 1 },
#     "a": { "c": 8 },
#     "b": { "a": 5, "c": 25, "e": 3 },
#     "c": { "d": 2, "b": 25 },
#     "d": { "e": 0 },
#     "e": { }
#   },
#   "nodes": {
#     "s": [0, 0],
#     "a": [1, 0],
#     "b": [1, 5],
#     "c": [9, 0],
#     "d": [11, 0],
#     "e": [5, 5]
#   }
# }


# получить узел, если это узел
def get_node(point, matrix, nodes):

    # Эта точка может быть узлом
    if matrix.data[point.y][point.x] == '1':

        # is it node?
        ways = find_possible_ways(matrix, point)
        ways_number = len(ways)

        # 1 путь - тупиковый узел
        # > 2 путей - обычный узел
        if ways_number == 1 or ways_number > 2 or point.vec in nodes:
            print(f'{point.vec} is node')
            for x in ways:
                print(f'neighbours : {x.vec}')

            # Чтобы не дублировать узлы
            if point.vec not in nodes:
                point_id = len(nodes)
                nodes[point.vec] = len(nodes)
            else:
                point_id = nodes[point.vec]
                print(f'{point.vec} already exist with id: {point_id}')
                ways = list()
            # True - это узел
            return nodes, Node(point_id, point, True, ways)
        # False - это не узел
        return nodes, Node(None, point, False, ways)

    ways = find_possible_ways(matrix, point)
    return nodes, Node(None, point, False, ways)


def will_wall_become_node(matrix, point):
    neighbours = list()
    vec_to_check = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

    for vec in vec_to_check:
        if ray_cast('0', vec, point, matrix):
            neighbours.append(Point(point.x + vec[0], point.y + vec[1]))

    if len(neighbours) > 0:
        return True
    else:
        return False


# получить узел, если это узел
def get_wall(point, matrix, walls):

    # Эта точка может быть стеной, которую мы сломаем
    if matrix.data[point.y][point.x] == '0':

        # будем ли ломать?
        ways = find_possible_ways(matrix, point)
        ways_number = len(ways)
        is_simple = will_wall_become_node(matrix, point)

        # > 1 путя - можем ломать!
        if ways_number > 1:
            print(f'{point.vec} wall to brake')
            for x in ways:
                print(f'neighbour way: {x.vec}')

            # Чтобы не дублировать узлы
            if point.vec not in walls:
                walls[point.vec] = Wall(point, ways, is_simple)
            else:
                point_id = walls[point.vec]
                print(f'{point.vec} already exist with id: {point_id}')
            return walls
        return walls
    return walls


def find_start_node(nodes, matrix):
    for r, c in rangend(len(matrix.data), len(matrix.data[0])):
        nodes, node = get_node(Point(c, r), matrix, nodes)
        if len(nodes) > 0:
            return nodes, node

    print("No nodes found")
    return nodes, Node(None, Point(None, None), False, list())


# Возможные пути по которым можно пойти от точки
def find_possible_ways(matrix, point):
    possible_ways = list()
    vec_to_check = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    for vec in vec_to_check:
        if ray_cast('1', vec, point, matrix):
            possible_ways.append(Point(point.x + vec[0], point.y + vec[1]))

    return possible_ways


def add_to_dict(adj, parent_node, new_node, way_len):

    if new_node.id not in adj:
        adj[new_node.id] = dict()

    if parent_node.id not in adj:
        adj[parent_node.id] = dict()

    adj[new_node.id][parent_node.id] = way_len
    adj[parent_node.id][new_node.id] = way_len

    return adj


def recursive_explorer(nodes_to_explore, matrix, nodes, adj):

    new_nodes_to_explore = list()
    # проходимся по всем узлам, которые имел пути
    for node in nodes_to_explore:

        # Проходимся по всем путям для этих узлов
        for point in node.neighbours:

            # сбрасываем переменные
            way_len = 0
            new_node = empty_node()
            point_to_explore = point
            previous_point = node.point
            # Пока не пришли к узлу
            # is_node позволяет избавиться от шастания по словарю всех узлов
            while not new_node.is_simple:
                nodes, new_node = get_node(point_to_explore, matrix, nodes)

                # Выкинем путь, ведущий назад
                new_node.neighbours = [x for x in new_node.neighbours if x.vec != previous_point.vec]

                # тут сохраняем текущую точку, чтобы потом
                # выкинуть путь ведущий назад
                new_node.parent_node = node.point
                previous_point = new_node.point

                # увеличим длинну пути
                way_len += 1

                # Если больше нет путей потыкаться, ливаем с катки
                if len(new_node.neighbours) == 0:
                    break

                point_to_explore = new_node.neighbours[0]

            # попали в узел, осталось сохранить данные
            adj = add_to_dict(adj, node, new_node, way_len)

            # сохраняем пути для будущего исследования
            new_nodes_to_explore.append(new_node)

    # Если больше некуда идти, то выходим
    # а если есть, то продолжаем
    if len(new_nodes_to_explore) > 0:
        recursive_explorer(new_nodes_to_explore, matrix, nodes, adj)

    return nodes, adj


def convert_to_graph(matrix):
    nodes = dict()
    adj = dict()

    # Находим стартовый узел от которого будет строить граф
    nodes, node = find_start_node(nodes, matrix)

    # снарядили экспедицию
    # добавили пути для исследования

    # разнюхиваем дорожки, идущие от узла
    nodes, adj = recursive_explorer([node], matrix, nodes, adj)

    walls_to_brake = find_walls(matrix)

    print(walls_to_brake)

    # инвертируем nodes, чтобы он представлял собой
    # свзяь id -> vec
    nodes = {v: list(k) for k, v in nodes.items()}

    return nodes, adj, walls_to_brake


def adjacency_matrix(adj):
    size = len(adj)
    matrix = [[None] * size for _ in range(size)]
    for node, links in adj.items():
        row = int(node)
        for other, length in links.items():
            col = int(other)
            matrix[row][col] = length
    return matrix


def empty_node():
    return Node(None, Point(None, None), False, list())


def load_from_json(path):
    graph = Graph()
    with open(path, "rt") as file:
        data = json.load(file)
        graph.nodes = data['Nodes']
        graph.adj = data['Adj']
        graph.adj_matrix = adjacency_matrix(graph.adj)
        return graph


def load_from_txt(path):
    graph = Graph()
    with open(path, "rt") as file:
        graph.matrix = Matrix([[it.strip() for it in it.strip()] for it in file.readlines()])

    graph.nodes, graph.adj, graph.walls_to_brake = convert_to_graph(graph.matrix)
    graph.adj_matrix = adjacency_matrix(graph.adj)
    return graph


def to_json(graph, path):
    with open(path, 'wt') as f:
        f.write(json.dumps(
            {
                'Nodes': graph.nodes,
                'Adj': graph.adj
            }, indent=4, sort_keys=True))


def rangend(*args: int) -> Iterator:
    return itertools.product(*(range(it) for it in args))


def arg_min(nodes_table, visited):
    amin = -1
    m = math.inf  # максимальное значение
    for i, t in enumerate(nodes_table):
        if t < m and i not in visited:
            m = t
            amin = i

    return amin


def dijkstra(end, start, adj_matrix, adj):

    tuple_matrix = tuple(tuple(x if x is not None else math.inf for x in x) for x in adj_matrix)

    nodes_number = len(tuple_matrix)  # число вершин в графе
    nodes_table = [math.inf] * nodes_number  # последняя строка таблицы

    start_node = start  # стартовая вершина (нумерация с нуля)
    visited = {start_node}  # просмотренные вершины
    nodes_table[start_node] = 0  # нулевой вес для стартовой вершины
    node_connections = [0] * nodes_number  # оптимальные связи между вершинами

    while start_node != -1:  # цикл, пока не просмотрим все вершины
        for j, dw in enumerate(tuple_matrix[start_node]):  # перебираем все связанные вершины с вершиной start_node
            if j not in visited:  # если вершина еще не просмотрена
                w = nodes_table[start_node] + dw
                if w < nodes_table[j]:
                    nodes_table[j] = w
                    node_connections[j] = start_node  # связываем вершину j с вершиной start_node

        start_node = arg_min(nodes_table, visited)  # выбираем следующий узел с наименьшим весом
        if start_node >= 0:  # выбрана очередная вершина
            visited.add(start_node)  # добавляем новую вершину в рассмотрение

    # формирование оптимального маршрута:
    optimal_route = [end]
    route_len = 0
    next_step = end

    while next_step != start:
        node = optimal_route[-1]
        next_step = node_connections[optimal_route[-1]]
        route_len += adj[node][next_step]
        optimal_route.append(next_step)

    print(f'Optimal_route: {optimal_route}')
    print(f'Route len: {route_len}')

    return optimal_route, route_len


# Возращает тру, если на коориданте находится target
def ray_cast(target, inc, point, matrix, radius=1):
    radius -= 1
    row = point.y + inc[1]
    col = point.x + inc[0]

    # Защита от выхода за пределы матрицы
    # if row >= 0 + radius or row <= matrix.rows - 1 + radius:
    if 0 + radius > row or row > matrix.rows - 1 + radius:
        return False
    if 0 + radius > col or col > matrix.columns - 1 + radius:
        return False

    if matrix.data[row][col] == target:
        return True
    else:
        return False


# найти все разрушаемые стенки лабиринта
def find_walls(matrix):
    walls = dict()
    for r, c in rangend(len(matrix.data), len(matrix.data[0])):
        walls = get_wall(Point(c, r), matrix, walls)
    return walls


def shortest_way(start, end, graph, brake_wall):

    # солнышко в руках
    # и венок из звёзд в небесах

    if start not in graph.adj:
        print(f'No {start} node in graph\nPlease, choose one of: {graph.nodes}')
        return graph

    if end not in graph.adj:
        print(f'No {end} node in graph\nPlease, choose one of: {graph.nodes}')
        return graph

    if graph.walls_to_brake is None:
        print('If you want to find new best way,\n',
              'please, load graph form txt file')

    best_route, best_len = dijkstra(start, end, graph.adj_matrix, graph.adj)
    best_graph = graph

    if brake_wall:

        # далее пригодится
        graph.nodes = {tuple(v): k for k, v in graph.nodes.items()}

        for wall_vec in graph.walls_to_brake:

            node_to_explore = graph.walls_to_brake[wall_vec]
            print(f'\nWhat if to brake {node_to_explore.point.vec} wall')

            # initialize current best
            new_graph = copy.deepcopy(graph)

            # brake the wall
            new_graph.matrix.data[node_to_explore.point.y][node_to_explore.point.x] = '1'

            if not node_to_explore.is_simple:

                # вместо стенки будет узел, так просто закинем его в recursive_explorer
                new_node_id = len(new_graph.adj)
                node_to_explore.id = new_node_id
                new_graph.nodes[node_to_explore.point.vec] = new_node_id
                new_graph.nodes, new_graph.adj = recursive_explorer([node_to_explore], new_graph.matrix,
                                                                    new_graph.nodes, new_graph.adj)

            else:
                # вместо стенки будет проход, запустим recursive_explorer для его соседей, чтобы нащупали друг-друга
                neighbours = [get_node(x, new_graph.matrix, new_graph.nodes)[1] for x in node_to_explore.neighbours]
                neighbours = [x for x in neighbours if x.id if not None]
                new_graph.nodes, new_graph.adj = recursive_explorer(neighbours, new_graph.matrix,
                                                                    new_graph.nodes, new_graph.adj)

            # Считаем длинну пути таекущей итерации графа
            new_graph.adj_matrix = adjacency_matrix(new_graph.adj)
            new_route, new_len = dijkstra(start, end, new_graph.adj_matrix, new_graph.adj)

            if new_len < best_len:
                best_graph = new_graph
                best_route = new_route
                best_len = new_len

        # Возвращае на место
        graph.nodes = {v: list(k) for k, v in graph.nodes.items()}

    print(f'Shortest way is: {best_route}\nwith len: {best_len}')

    # сохраним кратчайший путь
    best_graph.shortest_way = best_route
    best_graph.shortest_way_len = best_len

    return best_graph


class Wall(object):

    def __init__(self, point, neighbours, is_simple):
        self.point = point
        self.neighbours = neighbours
        self.id = None
        self.is_simple = is_simple

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Point: {self.point}, Neighbours: {self.neighbours}'


class Node(object):

    def __init__(self, node_id, point, is_simple, ways):
        self.point = point
        self.id = node_id
        self.is_simple = is_simple
        self.parent_node = Point(None, None)
        self.neighbours = ways

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Node (ID: {self.id}; Vec: {self.point.vec})'


class Matrix(object):

    def __init__(self, data):
        self.data = data
        self.rows = len(data)
        self.columns = len(data[0])


# В таком виде представляем клетку в лабиринте
class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vec = (self.x, self.y)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'Point (x:{self.x}, y:{self.y})'


class Graph(object):

    def __init__(self):
        self.matrix = None
        self.nodes = None
        self.adj = None
        self.adj_matrix = None
        self.walls_to_brake = None
        self.shortest_way = None
        self.shortest_way_len = None


def main():

    maze_1 = 'maze_01.txt'
    maze_2 = 'maze_02.txt'
    maze_3 = 'maze_03.txt'
    maze_4 = 'maze_04.txt'
    maze_6 = 'maze_06.txt'
    maze_7 = 'maze_07.txt'
    maze_8 = 'maze_08.txt'
    maze_9 = 'maze_09.txt'
    maze_json = 'maze_graph.json'

    # Читаем лабиринт из тхт файла
    graph = load_from_txt(maze_9)

    # Сохраняем граф в json
    to_json(graph, maze_json)

    # Загружаем граф из json
    graph2 = load_from_json(maze_json)

    # печатаем матрицу смежности
    for r in graph2.adj_matrix:
        print(r)

    best_graph = shortest_way(0, 3, graph, brake_wall=True)

    return 0


if __name__ == '__main__':
    main()

