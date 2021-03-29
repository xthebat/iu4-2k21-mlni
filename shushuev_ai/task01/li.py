from typing import Tuple, List, Iterable, Dict

from maze_tools import Maze, Point, Numeric
import maze_tools
import numpy as np


def adj_add_link(adj: Dict[Point, Dict[Point, Numeric]], root, node, length):
    if adj.get(root) is None:
        adj[root] = {node: length}
    else:
        adj[root][node] = length


class State(object):
    def __init__(self, maze: Maze, end: Point, start=None, queue=None, weight=None, visited=None, adj=None):
        self.maze = maze
        self.end = end
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

        self.queue_top_id = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.queue_top_id == len(self.queue):
            raise StopIteration

        root, curr = self.queue[self.queue_top_id]
        self.queue_top_id += 1

        self.visited.add(curr)

        unvisited = list(filter(lambda point: point not in self.visited and self.maze[point],
                                maze_tools.neighbours(self.maze, curr)))

        if (len(unvisited) != 1 or curr == self.end) and curr != root:
            # добавляем ребро
            adj_add_link(adj=self.adj, root=root, node=curr, length=self.weight_map[curr] - self.weight_map[root])
            root = curr

        for neigh in unvisited:
            self.queue.append((root, neigh))
            self.weight_map[neigh] = self.weight_map[curr] + self.maze[neigh]

        return curr

    def copy(self):
        """ Копирует состояние """
        if self.queue_top_id == 0:
            new_queue = self.queue.copy()
        else:
            new_queue = self.queue[self.queue_top_id - 1:].copy()

        return State(maze=self.maze.copy(),
                     end=self.end,
                     queue=new_queue,
                     weight=self.weight_map.copy(),
                     visited=self.visited.copy(),
                     adj={k: v.copy() for k, v in self.adj.items()})

