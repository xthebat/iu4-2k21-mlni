import json
import itertools
from typing import Iterator, List
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


def add_to_dict(adj, parent_node, new_node, way_len):

    if new_node.id not in adj:
        adj[new_node.id] = dict()

    if parent_node.id not in adj:
        adj[parent_node.id] = dict()

    adj[new_node.id][parent_node.id] = way_len
    adj[parent_node.id][new_node.id] = way_len

    return adj


def convert_to_graph(matrix):
    nodes = dict()
    adj = dict()

    # Находим стартовый узел от которого будет строить граф
    node = find_start_node(matrix)

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

    if brake_wall:

        # далее пригодится
        graph.nodes = {tuple(v): k for k, v in graph.nodes.items()}

        for wall_vec in graph.walls_to_brake:

            node_to_explore = graph.walls_to_brake[wall_vec]
            # initialize current best
            new_graph = copy.deepcopy(graph)

            # brake the wall
            new_graph.matrix.data[node_to_explore.point.y][node_to_explore.point.x] = '1'
            new_node_id = len(new_graph.adj)
            node_to_explore.id = new_node_id
            new_graph.nodes[node_to_explore.point.vec] = new_node_id

            # calculate new graph
            new_graph.nodes, new_graph.adj = recursive_explorer([node_to_explore], new_graph.matrix,
                                                                new_graph.nodes, new_graph.adj)

            # find shortest way
            new_graph.adj_matrix = adjacency_matrix(new_graph.adj)
            new_route, new_len = dijkstra(start, end, new_graph.adj_matrix, new_graph.adj)

            if new_len < best_len:
                graph = new_graph
                best_route = new_route
                best_len = new_len

    print(f'Shortest way is: {best_route}\nwith len: {best_len}')

    graph.nodes = {v: list(k) for k, v in graph.nodes.items()}

    return graph


class Wall(object):

    def __init__(self, point, neighbours):
        self.point = point
        self.neighbours = neighbours
        self.id = None

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


# В таком виде представляем клетку в лабиринте
class Point(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self is other:
            return True
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'(x:{self.x}, y:{self.y})'


class Matrix(object):

    @staticmethod
    def from_file(path):
        with open(path, "rt") as file:
            return Matrix([[it.strip() for it in it.strip()] for it in file.readlines()])

    def __init__(self, data: List[List]):
        self.__data = data
        self.rows = len(data)
        self.columns = len(data[0])

    def __getitem__(self, item):
        return self.__data[item[0]][item[1]]


class Maze(object):

    def __init__(self, matrix: Matrix):
        self.matrix = matrix
        self.nodes = dict()
        self.walls = dict()

    @property
    def rows(self):
        return self.matrix.rows

    @property
    def columns(self):
        return self.matrix.columns

    def find_start_node(self):
        for r, c in rangend(self.rows, self.columns):
            node = self.get_node(Point(c, r))
            if len(self.nodes) > 0:
                return node

        raise RuntimeError("No starting nodes found")

    # найти все разрушаемые стенки лабиринта
    def find_walls(self):
        for r, c in rangend(self.rows, self.columns):
            self.get_wall(Point(c, r))
        return self.walls

    def get_node(self, point):
        """получить узел, если это узел"""

        if self.matrix[point.y, point.x] != '1':
            ways = self.point_neighbours(point)
            return Node(None, point, False, ways)

        # is it node?
        ways = self.point_neighbours(point)
        ways_number = len(ways)

        # 1 путь - тупиковый узел
        # > 2 путей - обычный узел
        if ways_number == 1 or ways_number > 2:
            print(f'{point} is node')
            for it in ways:
                print(f'neighbours : {it}')

            # Чтобы не дублировать узлы
            if point not in self.nodes:
                point_id = len(self.nodes)
                self.nodes[point] = len(self.nodes)
            else:
                point_id = self.nodes[point]
                print(f'{point} already exist with id: {point_id}')
                ways = list()
            # True - это узел
            return Node(point_id, point, True, ways)
        # False - это не узел
        print(f'{point} is not node ')
        return Node(None, point, False, ways)

    def get_wall(self, point):
        """получить узел, если это узел"""

        # Эта точка может быть стеной, которую мы сломаем
        if self.matrix[point.y, point.x] == '0':

            # будем ли ломать?
            ways = self.point_neighbours(point)
            ways_number = len(ways)

            # > 1 путя - можем ломать!
            if ways_number > 1:
                print(f'{point} wall to brake')
                for way in ways:
                    print(f'neighbour way: {way}')

                # Чтобы не дублировать узлы
                if point not in self.walls:
                    point_id = len(self.walls)
                    self.walls[point] = Wall(point, ways)
                else:
                    point_id = self.walls[point]
                    print(f'{point.vec} already exist with id: {point_id}')
                return self.walls
            return self.walls
        return self.walls

    # Возможные пути по которым можно пойти от точки
    def point_neighbours(self, point):
        possible_ways = list()

        # check up
        if point.y != self.matrix.rows - 1:
            if self.ray_cast((0, 1), point):
                possible_ways.append(Point(point.x, point.y + 1))

        # check down
        if point.y != 0:
            if self.ray_cast((0, -1), point):
                possible_ways.append(Point(point.x, point.y - 1))

        # check left
        if point.x != 0:
            if self.ray_cast((-1, 0), point):
                possible_ways.append(Point(point.x - 1, point.y))

        # check right
        if point.x != self.columns - 1:
            if self.ray_cast((1, 0), point):
                possible_ways.append(Point(point.x + 1, point.y))

        return possible_ways

    def ray_cast(self, inc, point):
        """Возращает тру, если на коориданте находится 1"""
        return self.matrix[point.y + inc[1], point.x + inc[0]] == '1'

    def recursive_explorer(self, nodes_to_explore, nodes=None, adj=None):
        adj = adj or dict()
        nodes = nodes or list()

        new_nodes_to_explore = list()
        # проходимся по всем узлам, которые имел пути
        for node in nodes_to_explore:

            # Проходимся по всем путям для этих узлов
            for point in node.point_neighbours:

                # сбрасываем переменные
                way_len = 0
                new_node = empty_node()
                point_to_explore = point
                previous_point = node.point
                # Пока не пришли к узлу
                # is_node позволяет избавиться от шастания по словарю всех узлов
                while not new_node.is_simple:
                    new_node = self.get_node(point_to_explore)

                    # Выкинем путь, ведущий назад
                    new_node.point_neighbours = [x for x in new_node.point_neighbours if x.vec != previous_point.vec]

                    # тут сохраняем текущую точку, чтобы потом
                    # выкинуть путь ведущий назад
                    new_node.parent_node = node.point
                    previous_point = new_node.point

                    # увеличим длинну пути
                    way_len += 1

                    # Если больше нет путей потыкаться, ливаем с катки
                    if len(new_node.point_neighbours) == 0:
                        break

                    point_to_explore = new_node.point_neighbours[0]

                # попали в узел, осталось сохранить данные
                adj = add_to_dict(adj, node, new_node, way_len)

                # сохраняем пути для будущего исследования
                new_nodes_to_explore.append(new_node)

        # Если больше некуда идти, то выходим
        # а если есть, то продолжаем
        if len(new_nodes_to_explore) > 0:
            self.recursive_explorer(new_nodes_to_explore, nodes, adj)

        return nodes, adj


class Graph(object):

    @staticmethod
    def from_matrix(matrix):
        maze = Maze(matrix)
        node = maze.find_start_node()
        recursive_explorer([node], matrix, maze.nodes, adj)
        wall_to_brake = maze.find_walls()
        return Graph(nodes, adj, wall_to_brake)

    @staticmethod
    def from_file(path):
        return Graph.from_matrix(Matrix.from_file(path))

    def __init__(self, nodes, adj, wall_to_brake):
        self.matrix = None
        self.nodes = nodes
        self.adj = adj
        self.adj_matrix = adjacency_matrix(adj)
        self.walls_to_brake = wall_to_brake


def main():

    maze_1 = 'maze_01.txt'
    maze_2 = 'maze_02.txt'
    maze_3 = 'maze_03.txt'
    maze_4 = 'maze_04.txt'
    maze_6 = 'maze_06.txt'
    maze_7 = 'maze_07.txt'
    maze_json = 'maze_graph.json'

    # Читаем лабиринт из тхт файла
    graph = Graph.from_file(maze_7)

    print(f'Maze nodes: {graph.nodes}')
    print(f'Maze adj: {graph.adj}')
    print(f'Maze adj: {graph.adj_matrix}')

    # Сохраняем граф в json
    to_json(graph, maze_json)

    # Загружаем граф из json
    graph2 = load_from_json(maze_json)

    # печатаем матрицу смежности
    for r in graph2.adj_matrix:
        print(r)

    best_graph = shortest_way(1, 0, graph, brake_wall=True)

    return 0


if __name__ == '__main__':
    main()

