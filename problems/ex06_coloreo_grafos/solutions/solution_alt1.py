# Alternativa: verificando todos los adyacentes no solo los anteriores
def is_feasible(g, sol, node, color):
    for adj in g['g'][node]:
        if sol[adj] == color:
            return False
    return True

def coloring_va(g, m, sol, node):
    if node == g['n']:
        return sol, True
    for color in range(1, m+1):
        if is_feasible(g, sol, node, color):
            sol[node] = color
            sol, found = coloring_va(g, m, sol, node+1)
            if found:
                return sol, True
            sol[node] = 0
    return sol, False