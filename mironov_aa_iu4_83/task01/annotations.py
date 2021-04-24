from collections import namedtuple
from typing import List, Dict

Matrix = List[List[int]]
Point = namedtuple('Point', ['r', 'c'])  # (y, x)
PathFrom = namedtuple('PathFrom', ['node_id', 'side'])
HashId = int
Adjacency = Dict[Point, int]
