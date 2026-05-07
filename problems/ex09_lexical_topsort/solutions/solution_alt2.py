# Alternativa: con set ordenado manualmente en cada paso
def lexic_top_sort(g, n):
    in_degree = [0] * n
    for u in range(n):
        for v in g[u]:
            in_degree[v] += 1

    disponibles = sorted([i for i in range(n) if in_degree[i] == 0])
    result = []

    while disponibles:
        node = disponibles.pop(0)
        result.append(node)
        nuevos = []
        for adj in g[node]:
            in_degree[adj] -= 1
            if in_degree[adj] == 0:
                nuevos.append(adj)
        disponibles = sorted(disponibles + nuevos)

    if len(result) != n:
        print(-1)
        return

    print(*result)