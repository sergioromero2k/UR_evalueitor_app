from collections import deque

def bfs_aux(v, g, visited):
    visited[v] = True
    print(v, end=" ")
    q = deque()
    q.append(v)
    while q:
        aux = q.popleft()
        for adj in g[aux]:
            if not visited[adj]:
                q.append(adj)
                visited[adj] = True
                print(adj, end=" ")

def bfs(g):
    n = len(g) - 1
    visited = [False] * (n + 1)
    for v in range(1, n + 1):
        if not visited[v]:
            bfs_aux(v, g, visited)
    print()