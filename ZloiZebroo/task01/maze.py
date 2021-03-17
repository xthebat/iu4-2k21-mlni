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
def get_node(x, y, data, nodes):

    # Эта точка может быть узлом
    if data[y][x] == '1':

        # is it node?
        ways = find_possible_ways(data, (x, y))
        ways_number = len(ways)

        # 1 путь - тупиковый узел
        # > 2 путей - обычный узел
        if ways_number == 1 or ways_number > 2:
            print(f'x: {x}, y: {y} is node')

            # Чтобы не дублировать узлы
            if [x, y] not in nodes.values():
                point_id = len(nodes)
                nodes[point_id] = [x, y]
            else:
                point_id = list(nodes.values()).index([x, y])
                print(f'Already exist with id: {point_id}')
                ways = []
            # True - это узел
            return nodes, ways, True, Point(point_id, (x, y))
        # False - это не узел
        print(f'x: {x}, y: {y} is not node')
        return nodes, ways, False, Point(None, (x, y))

    ways = find_possible_ways(data, (x, y))
    return nodes, ways, False, Point(None, (x, y))


# найти все узлы лабиринта
def find_nodes(data):
    nodes = dict()

    last_y = len(data) - 1
    last_x = len(data[0]) - 1

    for y in range(len(data)):
        for x in range(len(data[0])):
            nodes, ways, is_node, point = get_node(x, y, data, nodes)

    return nodes


def find_start_node(data):
    nodes = dict()

    for y in range(len(data)):
        for x in range(len(data[0])):
            nodes, ways, is_node, previous_point = get_node(x, y, data, nodes)
            if len(nodes) > 0:
                print(f'Node found {nodes}')
                return nodes, ways, previous_point

    print("No nodes found")
    return nodes, [], Point(None, None)


# Возможные пути по которым можно пойти от точки
def find_possible_ways(data, point):
    possible_ways = list()
    x, y = point
    last_y = len(data) - 1
    last_x = len(data[0]) - 1

    # check up
    if y != last_y:
        if data[y + 1][x] == '1':
            possible_ways.append((x, y+1))

    # check down
    if y != 0:
        if data[y - 1][x] == '1':
            possible_ways.append((x, y-1))

    # check left
    if x != 0:
        if data[y][x - 1] == '1':
            possible_ways.append((x-1, y))

    # check right
    if x != last_x:
        if data[y][x + 1] == '1':
            possible_ways.append((x+1, y))

    return possible_ways


def add_to_dict(dc):
    if dc.point.id not in dc.adj:
        dc.adj[dc.point.id] = dict()

    if dc.previous_point.id not in dc.adj:
        dc.adj[dc.previous_point.id] = dict()

    # -1 так как считаем, что 2 соседних узла не имеют длинны
    # если между ними нет пустой клетки
    dc.adj[dc.point.id][dc.previous_point.id] = dc.way_len - 1
    dc.adj[dc.previous_point.id][dc.point.id] = dc.way_len - 1

    return dc.adj


def recursive_explorer(dc):

    # Загружаем новый список путей для исследования
    dc.current_ways = dc.next_explore
    dc.next_explore = list()

    # проходимся по всем узлам, которые имел пути
    for node in dc.current_ways:

        # Теперь текущий исследуемый узел становится предыдущим
        dc.previous_point = node.parent_node

        # Проходимся по всем путям для этих узлов
        for way in node.ways_to_explore:

            # Сохранили
            wte = WaysToExplore(None, dc.previous_point)

            x = way[0]
            y = way[1]
            # Пока не пришли к узлу
            # is_node позволяет избавиться от шастания по словарю всех узлов
            while not dc.is_node:
                dc.nodes, wte.ways_to_explore, dc.is_node, dc.point = get_node(x, y, dc.data, dc.nodes)

                # Выкинем путь, ведущий назад
                wte.ways_to_explore = [x for x in wte.ways_to_explore if x != wte.parent_node.vec]

                # тут сохраняем текущую точку, чтобы потом
                # выкинуть путь ведущий назад
                wte.parent_node = dc.point

                # увеличим длинну пути
                dc.way_len += 1

                # Если больше нет путей потыкаться, ливаем с катки
                if len(wte.ways_to_explore) == 0:
                    break

                # Новые Х и У, так как это не узел, путь у него 1
                x = wte.ways_to_explore[0][0]
                y = wte.ways_to_explore[0][1]

            # попали в узел, осталось сохранить данные
            print(f'Node found: {dc.point.vec}')
            dc.adj = add_to_dict(dc)

            # сохраняем пути для будущего исследования
            wte.parent_node = dc.point
            dc.next_explore.append(wte)

            # cбрасываем переменные
            dc.is_node = False
            dc.way_len = 0

    # Если больше некуда идти, то выходим
    # а если есть, то продолжаем
    if len(dc.next_explore) > 0 and dc.point.id < 10:
        recursive_explorer(dc)

    return dc


def convert_to_graph(data):

    # Находим стартовый узел от которого будет строить граф
    nodes, ways, previous_point = find_start_node(data)

    # снарядили экспедицию
    wte = WaysToExplore(ways, previous_point)
    dc = DataCase(data, nodes, wte.parent_node)
    # добавили пути для исследования
    dc.next_explore.append(wte)

    # разнюхиваем дорожки, идущие от узла
    recursive_explorer(dc)

    return dc.nodes, dc.adj


def adjacency_matrix(nodes, adj):
    adj_matrix = list()
    n = len(nodes)
    for x in range(n):

        string = list()
        for y in range(n):
            try:
                if str(y) in adj[str(x)]:
                    string.append(1)
                else:
                    string.append(0)
            except KeyError:
                if y in adj[x]:
                    string.append(1)
                else:
                    string.append(0)

        adj_matrix.append(string)

    return adj_matrix


def adjacency_matrix2(nodes, adj):
    size = len(adj)
    matrix = [[None] * size for _ in range(size)]
    for node, links in adj.items():
        row = int(node)
        for other, length in links.items():
            col = int(other)
            matrix[row][col] = length
    return matrix



# В таком виде представляем клетку в лабиринте
class Point:

    def __init__(self, point_id, vec):
        self.id = point_id
        self.vec = vec


# Сюда собираем пути, которые потом надо будет обойти
class WaysToExplore:

    def __init__(self, ways, parent):
        self.ways_to_explore = ways
        self.parent_node = parent


# Чтобы удобнее было таскать данные по функциям
class DataCase:

    def __init__(self, data, nodes, previous_point):
        self.data = data
        self.nodes = nodes
        self.adj = dict()
        self.current_ways = list()
        self.next_explore = list()
        self.point = None
        self.previous_point = previous_point
        self.way_len = 0
        self.is_node = False


class Maze(object):

    def __init__(self):
        self.matrix = None
        self.nodes = None
        self.adj = None
        self.adj_matrix = None

    def load_from_txt(self, txt_path):
        with open(txt_path, "rt") as file:
            self.matrix = [[it.strip() for it in it.strip()] for it in file.readlines()]

        # Если в лабиринте могут быть отрезанные пути за стенами
        # self.nodes = find_nodes(self.matrix)
        self.nodes, self.adj = convert_to_graph(self.matrix)
        self.adj_matrix = adjacency_matrix2(self.nodes, self.adj)

    def to_json(self, path):
        with open(path, 'wt') as f:
            # print(f'Nodes: {self.nodes}')
            # print(f'Connections: {self.adj}')
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
            self.adj_matrix = adjacency_matrix2(self.nodes, self.adj)


def main():

    maze_1 = 'maze_01.txt'
    maze_2 = 'maze_02.txt'
    maze_3 = 'maze_03.txt'
    maze_4 = 'maze_04.txt'
    maze_json = 'maze_graph.json'

    # Читаем лабиринт из тхт файла
    maze = Maze()
    maze.load_from_txt(maze_2)

    print(f'Maze matrix: {maze.matrix}')
    print(f'Maze nodes: {maze.nodes}')
    print(f'Maze adj: {maze.adj}')

    # Сохраняем граф в json
    maze.to_json(maze_json)

    # Загружаем граф из json
    maze2 = Maze()
    maze2.load_from_json(maze_json)

    # печатаем матрицу смежности
    for x in maze2.adj_matrix:
        print(x)

    return 0


if __name__ == '__main__':
    main()

