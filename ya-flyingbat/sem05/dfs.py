import json
from typing import Dict, Optional, Set


def dfs(adj: Dict, start: str, dist: int = 0, visited: Optional[Set[str]] = None):
    visited = visited or set()
    if start in visited:
        return
    visited.add(start)
    yield start, dist
    for other_node, other_dist in adj[start].items():
        yield from dfs(adj, other_node, dist + other_dist, visited)


def main():
    with open("adj.json", "rt") as file:
        txt = file.read()
        data = json.loads(txt)

    adj = data["adj"]

    for it in dfs(adj, "s"):
        print(it)


if __name__ == '__main__':
    main()
