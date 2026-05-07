# Alternativa: Prim con nodo inicial fijo en 1
def prim(g):
    n = len(g) - 1
    visited   = [False] * (n + 1)
    key       = [float("Inf")] * (n + 1)
    key[1]    = 0
    sol       = 0
    for _ in range(n):
        u = -1
        for v in range(1, n + 1):
            if not visited[v] and (u == -1 or key[v] < key[u]):
                u = v
        visited[u] = True
        sol += key[u]
        for src, dst, w in g[u]:
            if not visited[dst] and w < key[dst]:
                key[dst] = w
    return sol