# Alternativa: Kruskal con lista de aristas independiente (sin lista adyacencia)
def kruskal(g):
    seen = set()
    edges = []
    for adjs in g:
        for (src, dst, w) in adjs:
            key = (min(src, dst), max(src, dst))
            if key not in seen:
                seen.add(key)
                edges.append((w, src, dst))
    edges.sort()

    parent = list(range(len(g)))

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    sol = 0
    for w, u, v in edges:
        ru, rv = find(u), find(v)
        if ru != rv:
            parent[ru] = rv
            sol += w
    return sol