import sys
from typing import List


def read_map_from_csv(filename: str) -> List[List[int]]:
    file = open(filename, "rt")

    return [[int(num) for num in line.split(" ")] for line in file]


def main(args):
    filename = args[1] if len(args) > 1 else input("Enter path to csv file: ")

    m = read_map_from_csv(filename)

    print(m)


if __name__ == '__main__':
    main(sys.argv)
