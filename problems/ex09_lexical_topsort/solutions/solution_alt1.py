# Alternativa: usando heapq en vez de sort() en cada iteración
import heapq

def lexic_top_sort(g, n):
    in_degree = [0] * n
    for u in range(n):
        for v in g[u]:
            in_degree[v] += 1

    heap = [i for i in range(n) if in_degree[i] == 0]
    heapq.heapify(heap)
    result = []

    while heap:
        node = heapq.heappop(heap)
        result.append(node)
        for adj in g[node]:
            in_degree[adj] -= 1
            if in_degree[adj] == 0:
                heapq.heappush(heap, adj)

    if len(result) != n:
        print(-1)
        return

    print(*result)