import sys
import numpy as np
from typing import Tuple, Dict, Set
from maze_tools import Maze, Point, Numeric
import maze_tools
from li import State

Link = Tuple[Point, Point]


def adj_add_link(adj: Dict[Point, Dict[Point, Numeric]], root, node, length):
    if adj.get(root) is None:
        adj[root] = {node: length}
    else:
        adj[root][node] = length


def adj_from_maze(
        s: State,
        end: Point
) -> Dict[Point, Dict[Point, Numeric]]:
    for root, node in s:
        s.visited.add(node)
        unvisited = list(filter(lambda point: point not in s.visited and s.maze[point],
                                maze_tools.neighbours(s.maze, node)))

        if (len(unvisited) != 1 or node == end) and node != root:
            # добавляем ребро
            adj_add_link(adj=s.adj, root=root, node=node, length=s.weight_map[node] - s.weight_map[root])
            root = node

        # Если не обновить очередь итерация заглохнет
        s.update_queue(((root, neigh, s.weight_map[node] + s.maze[neigh]) for neigh in unvisited))

    return s.adj


def build_graph_from_maze_map(maze: Maze, start: Point, end: Point, break_wall=False):
    if break_wall:
        min_length = np.inf
        min_adj = dict()

        # do some magic
        for state in gen_break_wall_points(maze, start, end):
            adj = adj_from_maze(state, end)
            if state.weight_map[end] < min_length:
                min_length = state.weight_map[end]
                min_adj = adj

        return min_adj
    else:
        # в очереди хранятся пары корень, текущий узел
        s = State(maze, start)

        return adj_from_maze(s, end)


def neighs_has_pass(maze: Maze, visited: Set[Point], point: Point):
    return any(map(lambda it: it not in visited and maze[it], maze_tools.neighbours(maze, point)))


def neighs_get_passes(maze: Maze, visited: Set[Point], point: Point):
    return set(filter(lambda it: it not in visited and maze[it], maze_tools.neighbours(maze, point)))


def neighs_get_walls(maze: Maze, point: Point):
    return filter(lambda x: not maze[x], maze_tools.neighbours(maze, point))


def gen_break_wall_points(maze: Maze, start: Point, end: Point):
    state = State(maze=maze, start=start)
    for root, node in state:

        state.visited.add(node)
        unvisited = neighs_get_passes(state.maze, state.visited, node)

        # стены у которых есть непосещенные клетки с 1

        walls = filter(lambda w: neighs_has_pass(state.maze, state.visited, w), neighs_get_walls(state.maze, node))

        for wall in walls:
            new_state = state.copy()
            new_state.maze[wall] = 1
            new_state.queue.insert(0, (root, node))

            yield new_state

        if (len(unvisited) != 1 or node == end) and node != root:
            # добавляем ребро
            adj_add_link(adj=state.adj, root=root, node=node, length=state.weight_map[node] - state.weight_map[root])
            root = node

        # Если не обновить очередь итерация заглохнет
        state.update_queue(((root, neigh, state.weight_map[node] + state.maze[neigh]) for neigh in unvisited))


def main(args):
    if len(args) != 2:
        print("expected a path to maze file as first argument")
        exit(-1)

    filename = args[1]

    maze = maze_tools.from_file(filename)

    adj = build_graph_from_maze_map(maze, Point(row=0, col=0), Point(row=maze.rows() - 1, col=maze.cols() - 1), True)

    print(adj)


if __name__ == '__main__':
    main(sys.argv)
