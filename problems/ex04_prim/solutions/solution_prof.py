import random

def select_min(candidates, visited):
    node = None
    weight = float("Inf")
    for i in range(1, len(candidates)):
        if not visited[i] and candidates[i] < weight:
            node = i
            weight = candidates[i]
    return node, weight

def prim(g):
    n = len(g) - 1
    initial = random.randint(1, n)
    sol = 0
    visited = [False] * (n + 1)
    candidates = [float("Inf")] * (n + 1)
    for start, end, weight in g[initial]:
        candidates[end] = weight
    visited[initial] = True
    for _ in range(2, n + 1):
        next_node, cost = select_min(candidates, visited)
        if cost < float("Inf"):
            visited[next_node] = True
            sol += cost
        for start, end, weight in g[next_node]:
            if not visited[end]:
                candidates[end] = min(candidates[end], weight)
    return sol