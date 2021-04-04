import gc
import pstats
import time
from functools import reduce
from math import sqrt, pi
from profile import Profile
from typing import Dict, Callable


def observe(func: Callable):

    def wrapped(*args, **kwargs):
        result = func(*args, **kwargs)
        return result

    return wrapped


def profile(func):

    def wrap(*args, **kwargs):
        started_at = time.time()
        result = func(*args, **kwargs)
        print(time.time() - started_at)
        return result

    return wrap


# def profile(sort_args=['cumulative'], print_args=[10]):
#     profiler = Profile()
#
#     def decorator(fn):
#         def inner(*args, **kwargs):
#             result = None
#             try:
#                 result = profiler.runcall(fn, *args, **kwargs)
#             finally:
#                 stats = pstats.Stats(profiler)
#                 stats.strip_dirs().sort_stats(*sort_args).print_stats(*print_args)
#             return result
#         return inner
#
#     return decorator


class NamedDict(object):

    def __init__(self, d: Dict):
        self.__d = d

    def __getattr__(self, item):
        return self.__d[item]


class FuncGen(object):

    def __init__(self):
        pass

    def __getattr__(self, item):
        g = globals()
        return g[item]


class Point(object):

    def __map_zip(self, other, func):
        assert isinstance(other, Point)
        return map(func, zip(self.coords, other.coords))

    def _protected(self):
        pass

    # @staticmethod
    # def from_point(other):
    #     return Point(*other.coords)

    @classmethod
    def from_point(cls, other):
        return cls(*other.coords)

    def __init__(self, *args):
        self.coords = args

    def dot(self, other):
        return sum(self * other)

    def scalar(self):
        return self.dot(self)

    def distance2(self, other):
        assert isinstance(other, Point)
        return (self - other).scalar()

    def distance(self, other):
        return sqrt(self.distance2(other))

    @property
    def is_2d(self):
        return len(self.coords) == 2

    @property
    def x(self):
        return self.coords[0]

    @property
    def y(self):
        return self.coords[1]

    @property
    def z(self):
        return self.coords[2]

    def __del__(self):
        print(f"Deleting {self}")

    @profile
    @observe
    def __str__(self):
        return repr(self)

    def __repr__(self):
        return f"Point({', '.join(map(str, self.coords))})"

    def __add__(self, other):
        return Point(*self.__map_zip(other, lambda it: it[0] + it[1]))

    def __sub__(self, other):
        return Point(*self.__map_zip(other, lambda it: it[0] - it[1]))

    def __mul__(self, other):
        return Point(*self.__map_zip(other, lambda it: it[0] * it[1]))

    def __eq__(self, other):
        if self is other:
            return True
        return all(self.__map_zip(other, lambda it: it[0] == it[1]))

    def __lt__(self, other):
        return all(self.__map_zip(other, lambda it: it[0] < it[1]))

    def __le__(self, other):
        return all(self.__map_zip(other, lambda it: it[0] <= it[1]))

    def __len__(self):
        return len(self.coords)

    def __iter__(self):
        return iter(self.coords)

    def __getitem__(self, item):
        assert isinstance(item, int)
        return self.coords[item]


class AreaCalculatable(object):

    @classmethod
    def create(cls, *args):
        return cls(*args)

    def calc_area(self) -> float:
        raise NotImplementedError


class Rectangle(AreaCalculatable):

    def __init__(self, lb: Point, rt: Point):
        assert len(lb) == len(rt)
        assert lb < rt
        assert lb.is_2d
        assert rt.is_2d
        self.lb = lb
        self.rt = rt

    def __str__(self):
        return f"Rectangle({self.lb}, {self.rt})"

    def __getitem__(self, item):
        if item == 0:
            return Point.from_point(self.lb)
        elif item == 1:
            return Point(self.rt.x, self.lb.y)
        elif item == 2:
            return Point.from_point(self.rt)
        elif item == 3:
            return Point(self.lb.x, self.rt.y)
        else:
            raise IndexError("Unknown point index for Rectangle, must be 0 <= index < 4")

    def calc_area(self):
        return reduce(lambda x, y: x * y, self.rt - self.lb)


class Triangle(AreaCalculatable):

    def __init__(self, p0: Point, p1: Point, p2: Point):
        assert len(p0) == len(p1) == len(p2)
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2

    def __str__(self):
        return f"Triangle({self.p0}, {self.p1}, {self.p2})"

    def calc_area(self):
        return (self.rt - self.lb).scalar()


# Point.__str__ = observe(Point.__str__)


class Circle(AreaCalculatable):

    def __init__(self, center: Point, radius: int):
        assert len(center) == 2
        self.center = center
        self.radius = radius

    def __str__(self):
        return f"Circle({self.center}, {self.radius})"

    def calc_area(self):
        return pi * pow(self.radius, 2)


def other():
    d = NamedDict(dict(x=100, y=200, z=300))
    x = d.x
    print(f"x = {x}")
    f = FuncGen()
    f.geometry()


other = observe(other)


def geometry():
    # string = "%10.2f" % 14343.2
    # print(string)

    r0 = Rectangle.create(Point(10, 20), Point(20, 30))

    rect = Rectangle(Point(10, 20), Point(20, 30))
    # print(rect)
    p1 = Point(0, 0)
    p2 = Point(2, 2)
    print("Start ")

    del p1

    gc.collect()

    print(f"p2 = {p2}")

    p1 = Point(0, 1)

    print(f"p1[1] = {p1[1]}")

    points_sum = rect[0] + rect[1] + rect[2] + rect[3]
    print(f"{points_sum}")

    # dist = p1.distance(p2)
    # print(dist)
    # circle = Circle(Point(10, 20), 1)
    #
    #
    # figure = [rect, circle]
    #
    # for it in figure:
    #     print(f"area of {it} is {it.calc_area()}")

    # print([p1, p2])
    # print(p1)
    # print(p1 <= p2)
    # print(p1 == p1)
    # print(rect.calc_area())
    # print(circle.calc_area())


def main():
    geometry()
    # other()


if __name__ == '__main__':
    main()
