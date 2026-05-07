# Alternativa válida: visited como set, cola como lista
def bfs(g):
    n = len(g) - 1
    visited = set()
    output = []
    for start in range(1, n + 1):
        if start not in visited:
            visited.add(start)
            queue = [start]
            i = 0
            while i < len(queue):
                node = queue[i]
                output.append(node)
                for adj in g[node]:
                    if adj not in visited:
                        visited.add(adj)
                        queue.append(adj)
                i += 1
    print(*output)