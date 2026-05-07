# Alternativa: topsort iterativo con pila
def topsort(g):
    visited = set()
    result  = []

    def dfs(node):
        visited.add(node)
        for adj in g[node]:
            if adj not in visited:
                dfs(adj)
        result.append(node)

    for node in g:
        if node not in visited:
            dfs(node)

    print(*reversed(result))