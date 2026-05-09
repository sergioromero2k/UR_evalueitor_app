# Alternativa: con lista de visitados booleana
def hamiltonian_cycle_bt(g, v, sol):
    n = len(g)
    visited = [False] * n
    for node in sol:
        visited[node] = True

    if len(sol) == n:
        if sol[0] in g[v]:
            print(*(sol + [sol[0]]))
        return

    for adj in g[v]:
        if not visited[adj]:
            sol.append(adj)
            hamiltonian_cycle_bt(g, adj, sol)
            sol.pop()