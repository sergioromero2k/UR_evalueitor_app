# Alternativa válida: BFS con deque, sin función auxiliar
from collections import deque

def bfs(g):
    n = len(g) - 1
    visited = [False] * (n + 1)
    output = []
    for start in range(1, n + 1):
        if not visited[start]:
            visited[start] = True
            q = deque([start])
            while q:
                node = q.popleft()
                output.append(node)
                for adj in g[node]:
                    if not visited[adj]:
                        visited[adj] = True
                        q.append(adj)
    print(*output)