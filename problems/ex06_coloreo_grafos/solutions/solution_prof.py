def init_graph(n, adj):
    return {'n': n, 'g': adj}

def init_sol(g):
    return [0] * g['n']

def is_sol(g, node):
    return node == g['n']

def is_feasible(g, sol, node, color):
    for adj in g['g'][node]:
        if adj < node and sol[adj] == color:
            return False
    return True

def coloring_va(g, m, sol, node):
    if is_sol(g, node):
        found = True
    else:
        found = False
        color = 1
        while not found and color <= m:
            if is_feasible(g, sol, node, color):
                sol[node] = color
                sol, found = coloring_va(g, m, sol, node+1)
                if not found:
                    sol[node] = 0
            color += 1
    return sol, found