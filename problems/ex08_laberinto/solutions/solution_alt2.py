# Alternativa: DFS iterativo con pila
import copy

def is_feasible(lab, r, c):
    return (0 <= r < len(lab) and
            0 <= c < len(lab[0]) and
            lab[r][c] == 0)

def labyrinth(lab, best, r, c, k):
    n = len(lab)
    m = len(lab[0])

    def dfs(r, c, k):
        nonlocal best
        if r == n-1 and c == m-1:
            if lab[n-1][m-1] < best[n-1][m-1]:
                best = copy.deepcopy(lab)
            return
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = r+dr, c+dc
            if is_feasible(lab, nr, nc):
                lab[nr][nc] = k
                dfs(nr, nc, k+1)
                lab[nr][nc] = 0

    dfs(r, c, k)
    return best