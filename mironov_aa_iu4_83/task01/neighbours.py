from constants import SIDES
from utils import Adjacency, Paths, Nodes, Matrix, maze_contains, path_is_point_hash, path_get_node_id, \
    path_get_length, node_side_from_hash, path_get_point_side, path_has_point_side, maze_is_point_wall, \
    Point, point_add, point_sub, node_side_from_point


def find_paths(adj_dict: Adjacency, paths: Paths, nodes: Nodes, matrix: Matrix, point: Point) -> None:
    """ Check neighbours of node cell to find paths to other nodes """
    for side in SIDES:
        # DO NOT NEVER EVER USE NOTATION x, y FOR MATRIX, ALWAYS USE i, j OR BETTER r, c (row, col)
        # Because you in some place have (x, y) in others (y, x) it is f****ing crazy
        other = point_sub(point, side)

        if not maze_contains(matrix, other) or maze_is_point_wall(matrix, other):
            continue

        if other in nodes:
            # Neighbour is node -> path length = 1
            adj_dict[(nodes[other], nodes[point])] = 1

        if other in paths:
            if path_is_point_hash(paths, other):  # Neighbor is not a path to the node
                node_side_from_hash(side, nodes[point], paths, paths[other])
                if path_get_node_id(paths, other) == nodes[point]:
                    continue

            path_node = path_get_node_id(paths, other)
            link = (path_node, nodes[point])
            length = path_get_length(paths, paths[other])
            if link not in adj_dict:
                # The neighboring cell is exactly the path to the node
                adj_dict[link] = length

            elif adj_dict[link] > length:
                # There are two paths to one node -> choose the shortest path
                adj_dict[link] = length


def path_from_node(adj_dict: Adjacency, nodes: Nodes, matrix: Matrix, paths: Paths, point: Point) -> None:
    """ Check neighbours of path cell to find node membership """
    for side in SIDES:
        other = point_add(point, side)

        if not maze_contains(matrix, point) or maze_is_point_wall(matrix, point):
            continue

        if other in nodes:  # Neighbour is node
            paths[point] = node_side_from_point(nodes, other, side)

        elif other in paths:  # Neighbour is path
            if path_has_point_side(paths, point) and path_is_point_hash(paths, other):
                side = path_get_point_side(paths, point)
                ident = path_get_node_id(paths, point)
                node_side_from_hash(side, ident, paths, paths[other])
            elif path_has_point_side(paths, point) and not path_is_point_hash(paths, other):
                link = (path_get_node_id(paths, point), path_get_node_id(paths, other))
                length = path_get_length(paths, paths[point]) + path_get_length(paths, paths[other]) - 1
                adj_dict[link] = length
            else:
                paths[point] = paths[other]

        elif point not in paths:  # Current cell is not path
            paths[point] = hash(point)
