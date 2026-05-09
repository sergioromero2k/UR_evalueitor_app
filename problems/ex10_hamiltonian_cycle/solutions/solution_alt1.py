# Alternativa: con visited set
def hamiltonian_cycle_bt(g, v, sol):
    n = len(g)
    if len(sol) == n and sol[0] in g[v]:
        print(*(sol + [sol[0]]))
        return
    for adj in g[v]:
        if adj not in sol:
            sol.append(adj)
            hamiltonian_cycle_bt(g, adj, sol)
            sol.pop()