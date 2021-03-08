import itertools
import json
import jsonpickle
import socket
from typing import List, Dict, Tuple, Optional, Set
from sys import argv as SystemArguments
from ext import function

y = 100


def parse_csv(file):
    return [[int(it.strip()) for it in it.split(",")] for it in file.readlines()]


def matrix(filepath):
    with open(filepath, "rt") as file:
        csv = parse_csv(file)

    nodes = set()
    adj = dict()
    mat = dict()
    for (row, col) in itertools.product(range(len(csv)), repeat=2):

        if row - 1 > 0 and csv[row - 1][col]:
            pass
            # adj[]

        if col - 1 > 0:
            pass

        if csv[row][col]:
            mat[(row, col)] = 1

    print(mat)

    adj = {
        (0, 4): 1,
        (4, 0): 1,
        (4, 1): 1,
        (1, 4): 1,

        (1, 2): 2,
        (2, 1): 2,

        (2, 3): 2,
        (3, 2): 2
    }

    # mat = dict()
    # for k, row in enumerate(csv):
    #     for s, item in enumerate(row):
    #         if item:
    #             mat[(k, s)] = 1


def files(filename: str):
    file = open(filename, "rt")
    print(file.read())
    file.close()

    try:
        file = open(filename, "rt")
        csv = parse_csv(file)
    finally:
        file.close()

    print(csv)

    with open(filename, "rt") as file:
        csv = parse_csv(file)

    with socket.create_connection(address=("docs.python.org", 80)) as sock:
        sock.send(b"GET /")

    print(csv)


def else_break(args: List[str]):
    k = 0
    for it in args:
        if it.startswith("b"):
            break
        k += 1

    if k == len(args):
        print("else ...")

    flags = False
    for it in args:
        if it is None:
            continue
        if it.startswith("b"):
            break
    else:
        flags = True


def indexing(args):
    print(args[0])
    print(args[-2])
    print(args[2:])
    print(args[:-2])
    print(args[1:-2])


def exception(args: List[str]):
    # x = 10 / 0
    x = 10.0
    # assert type(x) == int, "Wrong type for x!"
    # assert isinstance(x, (int, float))
    # print(d["e"])

    # print(int("a"))

    result = dict()
    for it in args[1:]:
        name, value = it.split("=")
        result[name] = value
    print(result)

    try:
        d = {it[0]: function.convert(it[1]) for it in (it.split("=") for it in args[1:])}
    except ValueError:
        print("....")
        return -1

    filter(lambda it: it[1] is not None, d.items())


def locals_globals():
    x = 100

    print(dir())

    print(dir(x))

    print(x.to_bytes(10, byteorder="little"))

    print(locals())
    print(globals())

    g = globals()

    g["func"] = lambda it: it > 10

    print(func(10))
    print(func(11))

    print(globals())


def operator():
    d = dict(name="Alexei", group="IU4-33")

    if name := d.get("name"):
        print(name)


def main(args):
    matrix("lab.csv")
    # indexing(args)
    # exception(args)
    # files("lab.csv")


if __name__ == '__main__':
    main(SystemArguments)
