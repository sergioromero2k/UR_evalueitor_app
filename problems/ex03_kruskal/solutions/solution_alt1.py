# Alternativa: Kruskal con Union-Find por rango (path compression)
def kruskal(g):
    candidates = []
    for adjs in g:
        for (src, dst, w) in adjs:
            candidates.append((w, src, dst))
    candidates.sort()

    parent = list(range(len(g)))
    rank   = [0] * len(g)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x, y):
        rx, ry = find(x), find(y)
        if rx == ry:
            return False
        if rank[rx] < rank[ry]:
            rx, ry = ry, rx
        parent[ry] = rx
        if rank[rx] == rank[ry]:
            rank[rx] += 1
        return True

    sol = 0
    for w, src, dst in candidates:
        if union(src, dst):
            sol += w
    return sol