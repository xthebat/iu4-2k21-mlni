import csv

from annotations import Matrix
from models import Adjacency


def get_matrix(filename: str) -> Matrix:
    with open(filename, 'rt') as file:
        str_matrix = list(csv.reader(file))

    return [list(map(lambda x: int(x), str_matrix[i])) for i in range(len(str_matrix))]


def make_csv_matrix(adj: Adjacency) -> None:
    real_matrix = adj.to_dict()
    with open('adj.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerows(real_matrix)
