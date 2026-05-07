# Alternativa: con conjuntos de columnas y diagonales
def nqueens(sol, n, found, row):
    cols  = set(sol[:row])
    diag1 = set(sol[i] - i for i in range(row))
    diag2 = set(sol[i] + i for i in range(row))
    if row == n:
        return sol, True
    for col in range(n):
        if col not in cols and (col-row) not in diag1 and (col+row) not in diag2:
            sol[row] = col
            sol, found = nqueens(sol, n, found, row+1)
            if found:
                return sol, True
            sol[row] = -1
    return sol, False