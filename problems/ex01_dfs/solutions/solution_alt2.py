# Alternativa: DFS iterativo con pila explícita
def dfs(g):
    n = len(g) - 1
    visited = set()
    for start in range(1, n + 1):
        if start not in visited:
            stack = [start]
            order = []
            while stack:
                node = stack.pop()
                if node not in visited:
                    visited.add(node)
                    order.append(node)
                    for adj in reversed(g[node]):
                        if adj not in visited:
                            stack.append(adj)
            for node in order:
                print(f"Visiting node {node}")