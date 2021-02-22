import random
import sys
from typing import List, Dict, Optional


def max_length(values: List[int] = None):
    values = values or list()
    values.append(1)
    print(values)


def something(values: List[int]):
    if values:
        print("List is not empty!")
        return True
    return False


def decode_result(value: Dict):
    if len(value):
        return value
    return None
    # return value or None


def work_with_dict():
    d = {
        5: ["Ivan", "Maria"]
    }

    students4 = d.setdefault(4, [])
    students5 = d.setdefault(5, [])

    students4.append("Nikolay")
    students5.append("Alexey")

    print(d)


def length(string: str):
    print(f"Calc string length: {string}")
    return len(string)


def get_lengths_as_list(values: List[Optional[str]]):
    # results = []
    # for it in values:
    #     if it is not None:
    #         results.append(len(it))
    # return results
    return [length(it) for it in values if it is not None]


def get_lengths_as_generator_v0(values: List[Optional[str]]):
    return (length(it) for it in values if it is not None)


def get_lengths_as_generator_v1(values: List[Optional[str]]):
    for it in values:
        print(f"Checking value: {it}")
        if it is not None:
            yield length(it)


def work_with_comprehension(args):
    # print(get_lengths_as_list(args))
    gen = get_lengths_as_generator_v1(args)
    print(f"gen = {gen}")
    print(f"next = {next(gen)}")

    l1 = next((it for it in get_lengths_as_generator_v1(args) if it == 4), None)  # <- find { }

    next(it for it in get_lengths_as_generator_v1(args) if it == 4)  # <- first { }

    print(l1 is not None)

    # print(next(gen))
    # print(next(gen))
    # print(next(gen))
    # print(next(gen))

    # for it in gen:
    #     print(it)

    # print(next(gen, None))


def functional_programming(collection):
    # operator
    # collection
    # function
    #
    # function(operator, collection)

    func = lambda it: it < 0  # predicate  True or False

    lengths = map(lambda it: length(it), collection)  # (length(it) for it in values)

    # collection.filter { it != null }.map { it.length }.sorted()   # (length(it) for it in values if it is not None)

    lengths = sorted(
        map(
            lambda it: len(it),
            filter(
                lambda it: it is not None,
                collection
            )
        )
    )

    sorted_lengths = sorted(filter(lambda it: it is not None, collection), key=lambda it: len(it), reverse=True)

    print(list(sorted_lengths))

    if any(it is None for it in collection):
        print("We have someone is None!")

    if all(it is not None for it in collection):
        print("All elements is not None")

    # flag = False
    # for it in collection:
    #     if it is None:
    #         flag = True

    print(any([False, False, False]))
    print(any([False, True, False]))

    print(any([]))
    print(all([]))  # True

    print(max(1, 2, 3, 4))

    # for k in range(len(collection)):
    #     print(collection[k])

    for k in range(20):
        print(k)

    for k in range(20, 0, -1):
        print(f"k={k}")

    print(list(
        it % 12 for it in range(100)
    ))

    print(list(
        random.randint(0, 12) for _ in range(100)
    ))

    print(list(
        map(lambda it: it % 12, range(100))
    ))

    # for it in collection:
    #     print(it)


def main(args):
    # work_with_comprehension([None] + args)
    functional_programming(collection=[None] + args)


if __name__ == '__main__':
    main(sys.argv)
