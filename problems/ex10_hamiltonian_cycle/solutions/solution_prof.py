def is_sol(g, sol, v):
    return len(sol) == len(g) + 1 and sol[0] == v

def is_feasible(v, sol, n):
    return v not in sol or (v == sol[0] and len(sol) == n)

def hamiltonian_cycle_bt(g, v, sol):
    if is_sol(g, sol, v):
        print(*sol)
    else:
        for adj in g[v]:
            if is_feasible(adj, sol, len(g)):
                sol.append(adj)
                hamiltonian_cycle_bt(g, adj, sol)
                sol.pop()