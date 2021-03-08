import json
from typing import Dict, Optional, Set


def dfs(start: str, adj: Dict[str, Dict[str, int]], dist: int = 0, visited: Optional[Set[str]] = None):
    visited = visited or set()
    if start in visited:
        return
    visited.add(start)
    yield start, dist
    for other_node, other_dist in adj[start].items():
        yield from dfs(other_node, adj, dist + other_dist, visited)


def main():
    with open("adj.json", "rt") as file:
        data = json.loads(file.read())

    for node in dfs(start="s", adj=data["adj"]):
        print(node)


if __name__ == '__main__':
    main()
