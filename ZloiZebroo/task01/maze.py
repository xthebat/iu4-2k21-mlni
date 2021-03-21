import json

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
        if ways_number == 1 or ways_number > 2:
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
        print(f'{point.vec} is not node ')
        return nodes, Node(None, point, False, ways)

    ways = find_possible_ways(matrix, point)
    return nodes, Node(None, point, False, ways)


# найти все узлы лабиринта
# def find_nodes(data):
#     nodes = dict()
#
#     last_y = len(data) - 1
#     last_x = len(data[0]) - 1
#
#     for y in range(len(data)):
#         for x in range(len(data[0])):
#             nodes, ways, is_node, point = get_node(x, y, data, nodes)
#
#     return nodes


def find_start_node(nodes, matrix):

    for r in range(len(matrix.data)):
        for c in range(len(matrix.data[0])):
            nodes, node = get_node(Point(c, r), matrix, nodes)
            if len(nodes) > 0:
                return nodes, node

    print("No nodes found")
    return nodes, Node(None, Point(None, None), False, list())


# Возможные пути по которым можно пойти от точки
def find_possible_ways(matrix, point):
    possible_ways = list()

    # check up
    if point.y != matrix.rows - 1:
        if matrix.data[point.y + 1][point.x] == '1':
            possible_ways.append(Point(point.x, point.y+1))

    # check down
    if point.y != 0:
        if matrix.data[point.y - 1][point.x] == '1':
            possible_ways.append(Point(point.x, point.y-1))

    # check left
    if point.x != 0:
        if matrix.data[point.y][point.x - 1] == '1':
            possible_ways.append(Point(point.x-1, point.y))

    # check right
    if point.x != matrix.columns - 1:
        if matrix.data[point.y][point.x + 1] == '1':
            possible_ways.append(Point(point.x+1, point.y))

    return possible_ways


def add_to_dict(adj, parent_node, new_node, way_len):
    if new_node.id not in adj:
        adj[new_node.id] = dict()

    if parent_node.id not in adj:
        adj[parent_node.id] = dict()

    # -1 так как считаем, что 2 соседних узла не имеют длинны
    # если между ними нет пустой клетки
    adj[new_node.id][parent_node.id] = way_len - 1
    adj[parent_node.id][new_node.id] = way_len - 1

    return adj


def recursive_explorer(nodes_to_explore, matrix, nodes, adj):

    new_nodes_to_explore = list()
    # проходимся по всем узлам, которые имел пути
    for node in nodes_to_explore:

        # Проходимся по всем путям для этих узлов
        for point in node.neighbours:

            # cбрасываем переменные
            way_len = 0
            new_node = empty_node()
            # print(f'First point to explore {point.vec}')
            # print(f'First pprev potn {node.point.vec}')
            point_to_explore = point
            previous_point = node.point
            # Пока не пришли к узлу
            # is_node позволяет избавиться от шастания по словарю всех узлов
            while not new_node.is_simple:
                # print(f'point to explore{point_to_explore.vec}')
                nodes, new_node = get_node(point_to_explore, matrix, nodes)

                # print('eays_to_explore')
                # for x in new_node.ways_to_explore:
                #     print(x.vec)

                # print(f'prev point: {previous_point.vec}')
                # Выкинем путь, ведущий назад
                new_node.neighbours = [x for x in new_node.neighbours if x.vec != previous_point.vec]

                # print('eays_to_explore after clean')
                # for x in new_node.ways_to_explore:
                #     print(x.vec)
                # тут сохраняем текущую точку, чтобы потом
                # выкинуть путь ведущий назад
                new_node.parent_node = node.point
                previous_point = new_node.point

                # увеличим длинну пути
                way_len += 1

                # Если больше нет путей потыкаться, ливаем с катки
                if len(new_node.neighbours) == 0:
                    break

                # Новые Х и У, так как это не узел, путь у него 1
                # x = wte.ways_to_explore[0][0]
                # y = wte.ways_to_explore[0][1]
                # print(f'new node point: {new_node.ways_to_explore[0].vec}')
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

    # инвертируем nodes, чтобы он представлял собой
    # свзяь id -> vec
    nodes = {v: list(k) for k, v in nodes.items()}

    return nodes, adj


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


class Node(object):

    def __init__(self, node_id, point, is_simple, ways):
        self.point = point
        self.id = node_id
        self.is_simple = is_simple
        self.parent_node = Point(None, None)
        self.neighbours = ways


# class Graph:
#
#     def __init__(self):
#         self.nodes = None
#         self.connections = None
#         self.matrix = None


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


class Graph(object):

    def __init__(self):
        self.matrix = None
        self.nodes = None
        self.adj = None
        self.adj_matrix = None

    def load_from_txt(self, txt_path):
        with open(txt_path, "rt") as file:
            self.matrix = Matrix([[it.strip() for it in it.strip()] for it in file.readlines()])

        # Если в лабиринте могут быть отрезанные пути за стенами
        # self.nodes = find_nodes(self.matrix)
        self.nodes, self.adj = convert_to_graph(self.matrix)
        self.adj_matrix = adjacency_matrix(self.adj)

    def to_json(self, path):
        with open(path, 'wt') as f:
            f.write(json.dumps(
                {
                    'Nodes': self.nodes,
                    'Adj': self.adj
                }, indent=4, sort_keys=True))

    def load_from_json(self, json_path):
        with open(json_path, "rt") as file:
            data = json.load(file)
            self.nodes = data['Nodes']
            self.adj = data['Adj']
            self.adj_matrix = adjacency_matrix(self.adj)


def main():

    maze_1 = 'maze_01.txt'
    maze_2 = 'maze_02.txt'
    maze_3 = 'maze_03.txt'
    maze_4 = 'maze_04.txt'
    maze_json = 'maze_graph.json'

    # Читаем лабиринт из тхт файла
    graph = Graph()
    graph.load_from_txt(maze_2)

    print(f'Maze nodes: {graph.nodes}')
    print(f'Maze adj: {graph.adj}')

    # Сохраняем граф в json
    graph.to_json(maze_json)

    # Загружаем граф из json
    graph2 = Graph()
    graph2.load_from_json(maze_json)

    # печатаем матрицу смежности
    for r in graph2.adj_matrix:
        print(r)

    return 0


if __name__ == '__main__':
    main()

