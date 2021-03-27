from typing import Tuple, List, Iterable

from maze_tools import Maze, Point
import maze_tools
import numpy as np


class State(object):
    def __init__(self, maze: Maze, start=None, queue=None, weight=None, visited=None, adj=None):
        self.maze = maze
        if queue is None:
            self.queue = [(start, start)]
        else:
            self.queue = queue

        if weight is None:
            self.weight_map = maze_tools.from_value(rows=maze.rows(), cols=maze.cols(), value=np.inf)
            self.weight_map[start] = 0
        else:
            self.weight_map = weight

        if visited is None:
            self.visited = set()
        else:
            self.visited = visited

        if adj is None:
            self.adj = dict()
        else:
            self.adj = adj

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.queue) == 0:
            raise StopIteration

        root, curr = self.queue.pop(0)

        self.visited.add(curr)

        return root, curr

    def copy(self):
        """ Копирует состояние """
        return State(maze=self.maze.copy(),
                     queue=self.queue.copy(),
                     weight=self.weight_map.copy(),
                     visited=self.visited.copy(),
                     adj={k: v.copy() for k, v in self.adj.items()})

    def update_queue(self, paths: Iterable):
        for path in paths:
            prev, curr, weight = path
            self.queue.append((prev, curr))
            self.weight_map[curr] = weight
