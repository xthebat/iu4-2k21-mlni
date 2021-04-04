#!/home/andrey/MLNI/iu4-2k21-mlni/mironov_aa_iu4_83/env/bin/python
import sys

from annotations import Matrix
from csv_utils import make_csv_matrix, get_matrix
from dkstr import shortest_path
from models import Maze
from utils import benchmark, print_results


@benchmark
def main(path_to_file):
    matrix: Matrix = get_matrix(filename=path_to_file)

    maze = Maze(matrix)

    print_results(maze)

    make_csv_matrix(maze.adjacency, nodes_num=max(maze.nodes.values()) + 1)

    way, length = shortest_path()
    print(f'Minimal path: {way}, Length: {length}')


if __name__ == '__main__':
    path = sys.argv[1]
    main(path)
