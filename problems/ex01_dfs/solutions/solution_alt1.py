# Alternativa: visited como lista de booleanos en vez de set
def dfs_rec(v, g, visited):
    visited[v] = True
    print(f"Visiting node {v}")
    for u in g[v]:
        if not visited[u]:
            dfs_rec(u, g, visited)

def dfs(g):
    n = len(g) - 1
    visited = [False] * (n + 1)
    for v in range(1, n + 1):
        if not visited[v]:
            dfs_rec(v, g, visited)