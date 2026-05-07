# Alternativa: con conjunto de colores usados por vecinos
def coloring_va(g, m, sol, node):
    if node == g['n']:
        return sol, True
    used = set(sol[adj] for adj in g['g'][node] if sol[adj] != 0)
    for color in range(1, m+1):
        if color not in used:
            sol[node] = color
            sol, found = coloring_va(g, m, sol, node+1)
            if found:
                return sol, True
            sol[node] = 0
    return sol, False