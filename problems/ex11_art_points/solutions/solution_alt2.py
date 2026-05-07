# Alternativa: iterativa con pila explícita
def findArticulationPoints(g):
    n      = len(g)
    disc   = [-1] * n
    low    = [-1] * n
    parent = [-1] * n
    ap     = [False] * n
    timer  = [0]

    for start in range(n):
        if disc[start] != -1:
            continue
        stack    = [(start, 0)]
        children = [0] * n
        while stack:
            u, idx = stack[-1]
            if disc[u] == -1:
                disc[u] = low[u] = timer[0]
                timer[0] += 1
            if idx < len(g[u]):
                stack[-1] = (u, idx + 1)
                v = g[u][idx]
                if disc[v] == -1:
                    parent[v] = u
                    children[u] += 1
                    stack.append((v, 0))
                elif v != parent[u]:
                    low[u] = min(low[u], disc[v])
            else:
                stack.pop()
                if stack:
                    p = stack[-1][0]
                    low[p] = min(low[p], low[u])
                    if parent[p] == -1 and children[p] > 1:
                        ap[p] = True
                    if parent[p] != -1 and low[u] >= disc[p]:
                        ap[p] = True

    return sorted([i for i in range(n) if ap[i]])