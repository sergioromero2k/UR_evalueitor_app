def lexic_top_sort(g, n):
    aristas_entrantes = [0] * n
    for u in range(n):
        for v in g[u]:
            aristas_entrantes[v] += 1

    nodos_iniciales = [i for i in range(n) if aristas_entrantes[i] == 0]
    topological_sort = []
    cnt = 0

    while nodos_iniciales:
        nodos_iniciales.sort()
        origen = nodos_iniciales.pop(0)
        topological_sort.append(origen)
        for adj in g[origen]:
            aristas_entrantes[adj] -= 1
            if aristas_entrantes[adj] == 0:
                nodos_iniciales.append(adj)
        cnt += 1

    if cnt != n:
        print(-1)
        return

    print(*topological_sort)