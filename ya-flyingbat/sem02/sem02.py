import sys
import math
import json
import os
from typing import List, Optional


def get_max(collection: List[int]) -> Optional[int]:
    """
    Finds a maximum of collection

    :param collection: collection to find max
    :return: max or None if collection is empty
    """
    if len(collection) == 0:
        return None

    result = collection[0]
    for it in collection:
        if it > result:
            result = it

    return result


def get_min(collection):
    pass


def get_length(argument):
    return len(argument)


callbacks = {
    "max": get_max,
    "min": get_min,
}


def process(string: str) -> int:
    length = len(string)
    return length // 2 if length > 0 else -1


def transform(value):
    print(f"transforming {value}")
    return len(value)


def main(args):
    func_name = args[1]

    # args.filter { it != null }.map { len(it) }.associate { }
    lengths = [transform(it) for it in args if it is not None]
    # d = {it: len(it) for it in args if it is not None}

    print("=============================")

    lengths_gen = (transform(it) for it in args if it is not None)

    print(lengths_gen)

    next(lengths_gen)
    next(lengths_gen)

    result = []
    for it in args:
        if it is not None:
            result.append(len(it))

    print(lengths)

    if func_name not in callbacks:
        raise RuntimeError(f"Unknown function name: {func_name}")

    m = callbacks[func_name](list(map(int, args[2:])))

    if m is not None:
        print(f"m + 1 = {m + 1}")
    else:
        print(f"empty collection")


if __name__ == '__main__':
    main(sys.argv)
