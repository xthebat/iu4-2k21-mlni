import itertools
from typing import Optional, Iterator

d = dict()


def cut_between(string: str, start: str, end: str):
    return string[string.find(start) + len(string):string.rfind(end)]


def convert(string: str) -> Optional[int]:
    # try:
    #     return int(string)
    # except:
    #     pass

    try:
        print(f"trying to convert: {string}")
        value = int(string)
    except (ValueError, RuntimeError) as error:
        print(f"Can't convert value {string} due to: {error}")
        return None
    else:
        print("no exception")
        return value
    finally:
        print(f"Value done: {string}")


def rangend(*args: int) -> Iterator:
    return itertools.product(*(range(it) for it in args))
