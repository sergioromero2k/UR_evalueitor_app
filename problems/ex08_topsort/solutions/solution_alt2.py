# Alternativa: Kahn's algorithm (BFS topológico)
from collections import deque

def topsort(g):
    in_degree = {k: 0 for k in g}
    for u in g:
        for v in g[u]:
            in_degree[v] += 1

    queue = deque([k for k in g if in_degree[k] == 0])
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for adj in g[node]:
            in_degree[adj] -= 1
            if in_degree[adj] == 0:
                queue.append(adj)
    print(*result)