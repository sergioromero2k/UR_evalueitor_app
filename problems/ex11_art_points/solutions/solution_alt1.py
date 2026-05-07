# Alternativa: misma lógica pero con clase para evitar variables globales
def findArticulationPoints(g):
    n      = len(g)
    disc   = [-1] * n
    low    = [-1] * n
    parent = [-1] * n
    ap     = [False] * n
    timer  = [0]

    def dfs(u):
        disc[u] = low[u] = timer[0]
        timer[0] += 1
        children = 0
        for v in g[u]:
            if disc[v] == -1:
                children += 1
                parent[v] = u
                dfs(v)
                low[u] = min(low[u], low[v])
                if parent[u] == -1 and children > 1:
                    ap[u] = True
                if parent[u] != -1 and low[v] >= disc[u]:
                    ap[u] = True
            elif v != parent[u]:
                low[u] = min(low[u], disc[v])

    for i in range(n):
        if disc[i] == -1:
            dfs(i)

    return sorted([i for i in range(n) if ap[i]])