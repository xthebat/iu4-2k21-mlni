import sys
from typing import List


def parse_maze(file) -> List[List[int]]:
    return [[int(x) for x in line.split(', ')] for line in file]


def read_maze(path: str) -> List[List[int]]:
    with open(path) as file:
        return parse_maze(file)


def main(args):
    if len(args) < 2:
        print("введите путь до файла c лабиринтом: ")
        path = input()
    elif len(args) > 3:
        print("слишком много аргументов, введите название файла: ")
        path = input()
    else:
        path = args[1]

    maze = read_maze(path)

    print(maze)


if __name__ == '__main__':
    main(sys.argv)
