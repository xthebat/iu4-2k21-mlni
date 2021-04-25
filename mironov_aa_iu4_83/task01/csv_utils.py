import csv

from annotations import Matrix, Adjacency


def get_matrix(filename: str) -> Matrix:
    with open(filename, 'rt') as file:
        str_matrix = list(csv.reader(file))

    return [list(map(lambda x: int(x), str_matrix[i])) for i in range(len(str_matrix))]


def create_matrix_from_dict(adj: Adjacency, nodes_num: int) -> Matrix:
    real_matrix = [[0] * nodes_num for _ in range(nodes_num)]
    for x, y in adj.keys():
        real_matrix[x][y] = adj[(x, y)]
        real_matrix[y][x] = adj[(x, y)]
    return real_matrix


def make_csv_matrix(adj: Adjacency, nodes_num: int) -> None:
    real_matrix = create_matrix_from_dict(adj, nodes_num)
    with open('adj.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(real_matrix)