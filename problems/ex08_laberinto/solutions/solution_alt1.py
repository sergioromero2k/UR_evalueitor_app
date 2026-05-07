# Alternativa: BFS para encontrar el camino mas corto
import copy
from collections import deque

def labyrinth(lab, best, r, c, k):
    n = len(lab)
    m = len(lab[0])
    visited = [[False]*m for _ in range(n)]
    prev    = [[None]*m for _ in range(n)]
    queue   = deque([(0, 0, 1)])
    visited[0][0] = True

    while queue:
        row, col, step = queue.popleft()
        if row == n-1 and col == m-1:
            cur = (row, col)
            path = []
            while cur:
                path.append(cur)
                cur = prev[cur[0]][cur[1]]
            path.reverse()
            for idx, (pr, pc) in enumerate(path):
                best[pr][pc] = idx + 1
            return best
        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = row+dr, col+dc
            if 0<=nr<n and 0<=nc<m and not visited[nr][nc] and lab[nr][nc] != -1:
                visited[nr][nc] = True
                prev[nr][nc]    = (row, col)
                queue.append((nr, nc, step+1))
    return best