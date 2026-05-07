# Alternativa: usando set para verificar ataques
def nqueens(sol, n, found, row):
    if row == n:
        return sol, True
    for col in range(n):
        if _is_safe(sol, row, col):
            sol[row] = col
            sol, found = nqueens(sol, n, found, row+1)
            if found:
                return sol, True
            sol[row] = -1
    return sol, False

def _is_safe(sol, row, col):
    for i in range(row):
        if sol[i] == col:
            return False
        if abs(sol[i] - col) == abs(i - row):
            return False
    return True