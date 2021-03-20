from constants import SIDES
from utils import Adj_dict, Paths, Nodes, Matrix, pointer_in_maze_scope, cell_is_node, \
    cell_is_path, node_id_is_hash, node_id, get_path_length, get_corrections, make_node_side_from_hash


def find_paths(adj_dict: Adj_dict, paths: Paths, nodes: Nodes, matrix: Matrix, x: int, y: int) -> None:
    """ Check neighbours of node cell to find paths to other nodes """
    for side in SIDES:
        corr_x, corr_y = get_corrections(side, invert=True)

        if pointer_in_maze_scope(x + corr_x, y + corr_y, matrix) and matrix[y + corr_y][x + corr_x]:
            if cell_is_node(nodes, x + corr_x, y + corr_y):         # Neighbour is node -> path length = 1
                adj_dict.update({
                    (nodes[(x + corr_x, y + corr_y)], nodes[(x, y)]): 1
                })
            if cell_is_path(paths, x + corr_x, y + corr_y):         # Neighbor is path
                if node_id_is_hash(paths, x + corr_x, y + corr_y):  # Neighbor is not a path to the node
                    make_node_side_from_hash(side, nodes[(x, y)], paths, paths[(x + corr_x, y + corr_y)])
                    if node_id(paths, x + corr_x, y + corr_y) == nodes[(x, y)]:
                        continue
                if (node_id(paths, x + corr_x, y + corr_y), nodes[(x, y)]) not in adj_dict.keys():
                    # The neighboring cell is exactly the path to the node
                    adj_dict.update({
                        (
                            node_id(paths, x + corr_x, y + corr_y),
                            nodes[(x, y)]
                        ): get_path_length(paths, paths[(x + corr_x, y + corr_y)])
                    })
                else:
                    if adj_dict[(
                            node_id(paths, x + corr_x, y + corr_y),
                            nodes[(x, y)]
                    )] > get_path_length(paths, paths[(x + corr_x, y + corr_y)]):
                        # There are two paths to one node -> choose the shortest path
                        adj_dict.update({
                            (
                                node_id(paths, x + corr_x, y + corr_y),
                                nodes[(x, y)]
                            ): get_path_length(paths, paths[(x + corr_x, y + corr_y)])
                        })


def path_from_node(nodes: Nodes, matrix: Matrix, paths: Paths, x: int, y: int) -> None:
    """ Check neighbours of path cell to find node membership """
    for side in SIDES:
        corr_x, corr_y = get_corrections(side)

        if pointer_in_maze_scope(x + corr_x, y + corr_y, matrix) and matrix[y + corr_y][x + corr_x]:
            if cell_is_node(nodes, x + corr_x, y + corr_y):                 # Neighbour is node
                paths.update({(x, y): f'{nodes[(x + corr_x, y + corr_y)]}_{side}'})
            elif cell_is_path(paths, x + corr_x, y + corr_y):               # Neighbour is path
                paths.update({(x, y): paths[(x + corr_x, y + corr_y)]})
            elif (x, y) not in paths.keys():                                # Current cell is not path
                paths.update({(x, y): hash((x, y))})