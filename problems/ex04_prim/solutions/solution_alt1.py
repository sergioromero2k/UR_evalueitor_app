# Alternativa: Prim con heapq
import heapq

def prim(g):
    n = len(g) - 1
    visited = [False] * (n + 1)
    heap = [(0, 1)]
    sol = 0
    while heap:
        cost, u = heapq.heappop(heap)
        if visited[u]:
            continue
        visited[u] = True
        sol += cost
        for src, dst, w in g[u]:
            if not visited[dst]:
                heapq.heappush(heap, (w, dst))
    return sol