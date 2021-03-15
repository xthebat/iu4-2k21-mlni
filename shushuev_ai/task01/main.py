import sys
from typing import List, Dict, Generator


def generate_vertexes_from_file(filepath):
    file = open(filepath, "rt")
    row_gen = ([int(num) for num in line.split(' ')] for line in file)

    prev_row = None
    vid = 1
    for row in row_gen:
        prev = 0
        for i in range(len(row)):
            if row[i] == 1:
                row[i] = str(vid)
                vid += 1

                if prev == 1:
                    yield str(row[i - 1]), str(row[i])

                if prev_row is not None and prev_row[i] != 0:
                    yield str(prev_row[i]), str(row[i])

                prev = 1
            else:
                prev = 0

        prev_row = row


def build_graph_from_file_map(filepath) -> Dict[str, Dict[str, int]]:
    gen = generate_vertexes_from_file(filepath)

    adj = dict()
    for prev, curr in gen:
        if adj.get(prev) is None:
            adj[prev] = {curr: 1}
        else:
            adj[prev][curr] = 1

        # if adj.get(curr) is None:
            # adj[curr] = {prev: 1}
        # else:
            # adj[curr][prev] = 1

    return adj


def main(args):
    filename = args[1] if len(args) > 1 else input("Enter path to csv file: ")

    adj = build_graph_from_file_map(filename)

    print(adj)


if __name__ == '__main__':
    main(sys.argv)
