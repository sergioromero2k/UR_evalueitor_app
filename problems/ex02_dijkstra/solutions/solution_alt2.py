# Alternativa: Dijkstra con diccionario de distancias
def dijkstra(g, start):
    n = len(g) - 1
    INF = 0x3f3f3f3f
    dist    = {i: INF for i in range(1, n + 1)}
    visited = {i: False for i in range(1, n + 1)}
    dist[start] = 0

    for _ in range(n):
        u = min((v for v in range(1, n+1) if not visited[v]),
                key=lambda v: dist[v])
        visited[u] = True
        for src, dst, w in g[u]:
            if dist[u] + w < dist[dst]:
                dist[dst] = dist[u] + w

    return [0] + [dist[i] for i in range(1, n + 1)]