# Alternativa: Dijkstra con heapq (más eficiente)
import heapq

def dijkstra(g, start):
    n = len(g) - 1
    INF = 0x3f3f3f3f
    distances = [INF] * (n + 1)
    distances[start] = 0
    heap = [(0, start)]
    while heap:
        dist, u = heapq.heappop(heap)
        if dist > distances[u]:
            continue
        for src, dst, w in g[u]:
            if distances[u] + w < distances[dst]:
                distances[dst] = distances[u] + w
                heapq.heappush(heap, (distances[dst], dst))
    return distances