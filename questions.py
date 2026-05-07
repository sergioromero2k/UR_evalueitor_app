# questions.py — Banco de preguntas EVALUEITOR
# Algoritmos del profesor + enunciados de prácticas

# ─────────────────────────────────────────────────────────
#  ESTRUCTURA DE CADA PREGUNTA
# ─────────────────────────────────────────────────────────
# {
#   "id": str,
#   "name": str,
#   "type": "A" | "B",        A = implementa algoritmo, B = procesa datos
#   "topic": str,
#   "enunciado": str,
#   "prof_code": str,         código del profesor (para diff)
#   "test_cases": [           para tests automáticos
#       {"input": str, "expected_output": str, "description": str}
#   ]
# }

QUESTIONS_P1 = [
    # ─── BFS ────────────────────────────────────────────
    {
        "id": "bfs",
        "name": "BFS — Búsqueda en Anchura",
        "type": "A",
        "topic": "grafos",
        "enunciado": """Implementa el algoritmo BFS (Breadth-First Search) del profesor.

El grafo está representado como lista de adyacencia (índice 0 vacío).
Debes manejar grafos no conexos (varios componentes).

FUNCIONES REQUERIDAS:
  bfs_aux(v, g, visited)  → recorre desde el nodo v en anchura
  bfs(g)                  → llama bfs_aux para todos los nodos no visitados

EJEMPLO DE USO:
  g = [[], [2,4,8], [1,3,4], [2,4,5], [1,2,3,7], [3,6], [5,7], [4,6,9], [1,9], [7,8]]
  bfs(g)
  Salida: 1 2 4 8 3 7 9 5 6 (orden BFS desde cada componente)

NOTAS:
  • Usa collections.deque para la cola
  • visited es una lista de booleanos indexada por nodo
  • n = len(g)-1 (porque índice 0 está vacío)""",
        "prof_code": """from collections import deque

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
    n = len(g)-1
    visited = [False] * (n+1)
    for v in range(1, n+1):
        if not visited[v]:
            bfs_aux(v, g, visited)""",
        "test_cases": [
            {
                "setup": """
from collections import deque
g = [[], [2,3], [1,3], [1,2]]
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": "bfs(g)",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "set(captured.getvalue().split()) == {'1','2','3'}",
                "description": "BFS sobre triángulo (nodos 1,2,3)",
            },
            {
                "setup": """
from collections import deque
g = [[], [2], [1], [4], [3]]
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": "bfs(g)",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "len(captured.getvalue().split()) == 4",
                "description": "BFS con 2 componentes conexos",
            },
        ],
    },
    # ─── DFS ────────────────────────────────────────────
    {
        "id": "dfs",
        "name": "DFS — Búsqueda en Profundidad",
        "type": "A",
        "topic": "grafos",
        "enunciado": """Implementa el algoritmo DFS recursivo del profesor.

El grafo usa lista de adyacencia (índice 0 vacío).
Debes manejar grafos no conexos.

FUNCIONES REQUERIDAS:
  dfs_rec(v, g, visited)  → DFS recursivo desde nodo v (visited es un set)
  dfs(g)                  → itera todos los nodos llamando dfs_rec

EJEMPLO DE USO:
  g = [[], [2,4,8], [1,3,4], [2,4,5], [1,2,3,7], [3,6], [5,7], [4,6,9], [1,9], [7,8]]
  dfs(g)
  Imprime: Visiting node X para cada nodo

NOTAS:
  • visited es un SET (no lista de booleanos como en BFS)
  • Imprime f"Visiting node {v}" al entrar en cada nodo""",
        "prof_code": """def dfs_rec(v, g, visited):
    visited.add(v)
    print(f"Visiting node {v}")
    for u in g[v]:
        if u not in visited:
            dfs_rec(u, g, visited)

def dfs(g):
    n = len(g)-1
    visited = set()
    for v in range(1, n+1):
        if v not in visited:
            dfs_rec(v, g, visited)""",
        "test_cases": [
            {
                "setup": """
g = [[], [2,3], [1,3], [1,2]]
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": "dfs(g)",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "len(captured.getvalue().strip().split('\\n')) == 3",
                "description": "DFS visita exactamente 3 nodos en triángulo",
            },
        ],
    },
    # ─── DIJKSTRA ───────────────────────────────────────
    {
        "id": "dijkstra",
        "name": "Dijkstra — Caminos Mínimos",
        "type": "A",
        "topic": "grafos",
        "enunciado": """Implementa el algoritmo de Dijkstra del profesor.

El grafo es lista de adyacencia con tuplas (src, dst, weight). Índice 0 vacío.
Usa 0x3f3f3f3f como valor de infinito.

FUNCIONES REQUERIDAS:
  select_min(distances, visited) → devuelve índice del nodo no visitado con menor distancia
  dijkstra(g, start)             → devuelve lista distances[] con distancias mínimas desde start

EJEMPLO:
  g = [[], [(1,2,5),(1,4,3)], [(2,5,1)], [], [(4,2,1),(4,3,11),(4,5,6)], [(5,3,1)]]
  dijkstra(g, 1)
  → [0x3f3f3f3f, 0, 4, 6, 3, 5]  (distancias desde nodo 1)

NOTAS:
  • El grafo es DIRIGIDO (aristas con dirección)
  • distances[start] = 0, resto = 0x3f3f3f3f
  • select_min ignora nodos ya visitados""",
        "prof_code": """def select_min(distances, visited):
    next_node = 0
    min_dist = 0x3f3f3f3f
    for i in range(1, len(distances)):
        if not visited[i] and distances[i] < min_dist:
            next_node = i
            min_dist = distances[i]
    return next_node

def dijkstra(g, start):
    n = len(g)-1
    distances = [0x3f3f3f3f] * (n+1)
    visited = [False] * (n+1)
    distances[start] = 0
    visited[start] = True
    for src, dst, w in g[start]:
        distances[dst] = w
    for _ in range(2, n+1):
        next_node = select_min(distances, visited)
        visited[next_node] = True
        for src, dst, w in g[next_node]:
            distances[dst] = min(distances[dst], distances[src]+w)
    return distances""",
        "test_cases": [
            {
                "setup": """
g = [[], [(1,2,5),(1,4,3)], [(2,5,1)], [], [(4,2,1),(4,3,11),(4,5,6)], [(5,3,1)]]
""",
                "call": "result = dijkstra(g, 1)",
                "restore": "",
                "check": "result[2] == 4 and result[3] == 6 and result[4] == 3 and result[5] == 5",
                "description": "Distancias desde nodo 1: 2→4, 3→6, 4→3, 5→5",
            },
            {
                "setup": """
g = [[], [(1,2,10)], [(2,3,5)], []]
""",
                "call": "result = dijkstra(g, 1)",
                "restore": "",
                "check": "result[1] == 0 and result[2] == 10 and result[3] == 15",
                "description": "Camino lineal 1→2→3: distancias 0,10,15",
            },
        ],
    },
    # ─── PRIM ────────────────────────────────────────────
    {
        "id": "prim",
        "name": "Prim — Árbol de Expansión Mínima",
        "type": "A",
        "topic": "grafos",
        "enunciado": """Implementa el algoritmo de Prim del profesor para encontrar el MST.

El grafo es lista de adyacencia con tuplas (start, end, weight). Índice 0 vacío.

FUNCIONES REQUERIDAS:
  select_min(candidates, visited) → nodo no visitado con menor coste candidato
  prim(g)                         → devuelve coste total del MST

EJEMPLO:
  g = [[], [(1,3,1),(1,4,2),(1,7,6)], [(2,5,2),(2,6,4),(2,7,7)],
       [(3,1,1),(3,4,3),(3,7,5)], [(4,1,2),(4,3,3),(4,5,1),(4,6,9)],
       [(5,2,2),(5,4,1),(5,7,8)], [(6,2,4),(6,4,9)],
       [(7,1,6),(7,2,7),(7,3,5),(7,5,8)]]
  prim(g) → 14  (coste del MST)

NOTAS:
  • Nodo inicial: random.randint(1, n-1)
  • candidates[i] = menor coste conocido para llegar al nodo i
  • El resultado puede variar (nodo inicial aleatorio) pero el coste es siempre el mismo""",
        "prof_code": """import random

def select_min(candidates, visited):
    node = None
    weight = float("Inf")
    for i in range(1, len(candidates)):
        if not visited[i] and candidates[i] < weight:
            node = i
            weight = candidates[i]
    return node, weight

def prim(g):
    n = len(g)
    initial = random.randint(1, n-1)
    sol = 0
    visited = [False] * n
    candidates = [float("Inf")] * n
    for start, end, weight in g[initial]:
        candidates[end] = weight
    visited[initial] = True
    for _ in range(2, n):
        next_node, cost = select_min(candidates, visited)
        if cost < float("Inf"):
            visited[next_node] = True
            sol += cost
        for start, end, weight in g[next_node]:
            if not visited[end]:
                candidates[end] = min(candidates[end], weight)
    return sol""",
        "test_cases": [
            {
                "setup": """
import random
random.seed(42)
g = [[], [(1,3,1),(1,4,2),(1,7,6)], [(2,5,2),(2,6,4),(2,7,7)],
     [(3,1,1),(3,4,3),(3,7,5)], [(4,1,2),(4,3,3),(4,5,1),(4,6,9)],
     [(5,2,2),(5,4,1),(5,7,8)], [(6,2,4),(6,4,9)],
     [(7,1,6),(7,2,7),(7,3,5),(7,5,8)]]
""",
                "call": "result = prim(g)",
                "restore": "",
                "check": "result == 14",
                "description": "MST del grafo de 7 nodos → coste 14",
            },
        ],
    },
    # ─── KRUSKAL ─────────────────────────────────────────
    {
        "id": "kruskal",
        "name": "Kruskal — Árbol de Expansión Mínima",
        "type": "A",
        "topic": "grafos",
        "enunciado": """Implementa el algoritmo de Kruskal del profesor para el MST.

El grafo es lista de adyacencia con tuplas (src, dst, weight). Índice 0 vacío.
Usa componentes (Union-Find simplificado sin path compression).

FUNCIONES REQUERIDAS:
  sort_candidates(g)                           → lista de (w, src, dst) ordenada
  update_components(components, new_id, old_id) → actualiza todos los old_id a new_id
  kruskal(g)                                   → devuelve coste total del MST

EJEMPLO:
  (mismo grafo que Prim)
  kruskal(g) → 14

NOTAS:
  • Ordena todas las aristas por peso
  • Añade arista si conecta componentes distintos
  • update_components recorre toda la lista para cambiar el identificador""",
        "prof_code": """def sort_candidates(g):
    candidates = []
    for adjs in g:
        for (src, dst, w) in adjs:
            candidates.append((w, src, dst))
    candidates.sort()
    return candidates

def update_components(components, new_id, old_id):
    for i in range(len(components)):
        if components[i] == old_id:
            components[i] = new_id

def kruskal(g):
    candidates = sort_candidates(g)
    components = list(range(len(g)))
    number_components = len(components)
    sol = 0
    i = 0
    while i < len(candidates) and number_components > 1:
        w, src, dst = candidates[i]
        if components[src] != components[dst]:
            sol += w
            number_components -= 1
            update_components(components, components[src], components[dst])
        i += 1
    return sol""",
        "test_cases": [
            {
                "setup": """
g = [[], [(1,3,1),(1,4,2),(1,7,6)], [(2,5,2),(2,6,4),(2,7,7)],
     [(3,1,1),(3,4,3),(3,7,5)], [(4,1,2),(4,3,3),(4,5,1),(4,6,9)],
     [(5,2,2),(5,4,1),(5,7,8)], [(6,2,4),(6,4,9)],
     [(7,1,6),(7,2,7),(7,3,5),(7,5,8)]]
""",
                "call": "result = kruskal(g)",
                "restore": "",
                "check": "result == 14",
                "description": "MST grafo 7 nodos → coste 14",
            },
            {
                "setup": """
g = [[], [(1,2,4),(1,3,2)], [(2,1,4),(2,3,1)], [(3,1,2),(3,2,1)]]
""",
                "call": "result = kruskal(g)",
                "restore": "",
                "check": "result == 3",
                "description": "Triángulo con pesos 4,2,1 → MST=3",
            },
        ],
    },
    # ─── SCHEDULING ──────────────────────────────────────
    {
        "id": "scheduling",
        "name": "Scheduling — Planificación de Tareas",
        "type": "A",
        "topic": "voraz",
        "enunciado": """Implementa el algoritmo greedy de scheduling del profesor.
Maximiza el beneficio total asignando tareas a slots de tiempo antes de su deadline.

FUNCIONES REQUERIDAS:
  get_best_item(candidates, profit) → índice de la tarea con mayor beneficio
  greedy_schedule(profit, deadline) → devuelve sol[] con índice de tarea por slot

EJEMPLO:
  profit = [50, 10, 15, 30]
  deadline = [2, 1, 2, 1]
  sol = greedy_schedule(profit, deadline)
  # sol[0]=-1, sol[1]=3(Borja30), sol[2]=0(Manuel50) ← selección greedy

NOTAS:
  • sol es de tamaño (max_deadline + 1), índice 0 no se usa
  • Asigna la tarea al slot más tardío disponible antes de su deadline
  • Si no hay slot libre, la tarea no se asigna""",
        "prof_code": """def get_best_item(candidates, profit):
    best_item = -1
    best_profit = -1
    for c in candidates:
        if profit[c] > best_profit:
            best_profit = profit[c]
            best_item = c
    return best_item

def greedy_schedule(profit, deadline):
    n = len(profit)
    candidates = set()
    for i in range(n):
        candidates.add(i)
    last_date = max(deadline)
    sol = [-1] * (last_date+1)
    j = 0
    while candidates and j <= last_date:
        best = get_best_item(candidates, profit)
        candidates.remove(best)
        i = deadline[best]
        found = False
        while i > 0 and not found:
            if sol[i] == -1:
                sol[i] = best
                found = True
            i -= 1
        j += 1
    return sol""",
        "test_cases": [
            {
                "setup": """
profit = [50, 10, 15, 30]
deadline = [2, 1, 2, 1]
""",
                "call": "sol = greedy_schedule(profit, deadline)",
                "restore": "",
                "check": "sum(profit[s] for s in sol if s != -1) == 80",
                "description": "Beneficio máximo debe ser 80 (tareas 0 y 3)",
            },
            {
                "setup": """
profit = [100, 20]
deadline = [1, 1]
""",
                "call": "sol = greedy_schedule(profit, deadline)",
                "restore": "",
                "check": "0 in sol and sum(profit[s] for s in sol if s != -1) == 100",
                "description": "Solo cabe 1 tarea en deadline=1, elige la de mayor beneficio",
            },
        ],
    },
    # ─── WAITING TIME ────────────────────────────────────
    {
        "id": "waiting_time",
        "name": "Waiting Time — Minimizar Tiempo de Espera",
        "type": "A",
        "topic": "voraz",
        "enunciado": """Implementa el algoritmo de minimización de tiempo de espera del profesor.
Ordena tareas de menor a mayor duración para minimizar la espera acumulada.

FUNCIONES REQUERIDAS:
  get_best_task(candidates, tasks)   → índice de la tarea con MENOR duración
  order_tasks(tasks)                 → lista de índices en orden óptimo
  calculate_waiting_time(sol, tasks) → imprime tiempos acumulados y suma total

EJEMPLO:
  tasks = [5, 10, 3]
  sol = order_tasks(tasks)    → [2, 0, 1]  (orden: 3, 5, 10)
  calculate_waiting_time(sol, tasks)
  → [3, 8, 18]
  → 29

NOTAS:
  • get_best_task devuelve el de MENOR tiempo (al contrario que scheduling)
  • El tiempo acumulado se va sumando tarea a tarea""",
        "prof_code": """def get_best_task(candidates, tasks):
    best_task = 0
    best_task_time = 0x3f3f3f3f
    for c in candidates:
        if tasks[c] < best_task_time:
            best_task = c
            best_task_time = tasks[c]
    return best_task

def order_tasks(tasks):
    candidates = set()
    for i in range(len(tasks)):
        candidates.add(i)
    sol = []
    while candidates:
        best = get_best_task(candidates, tasks)
        candidates.remove(best)
        sol.append(best)
    return sol

def calculate_waiting_time(sol, tasks):
    times = []
    accum = 0
    for i in range(len(sol)):
        task = sol[i]
        accum += tasks[task]
        times.append(accum)
    print(times)
    print(sum(times))""",
        "test_cases": [
            {
                "setup": "tasks = [5, 10, 3]",
                "call": "sol = order_tasks(tasks)",
                "restore": "",
                "check": "sol == [2, 0, 1]",
                "description": "Orden óptimo de tasks=[5,10,3] → [2,0,1]",
            },
            {
                "setup": "tasks = [5, 10, 3]",
                "call": """
sol = order_tasks(tasks)
times = []
accum = 0
for t in sol:
    accum += tasks[t]
    times.append(accum)
result = sum(times)
""",
                "restore": "",
                "check": "result == 29",
                "description": "Suma de tiempos de espera debe ser 29",
            },
        ],
    },
    # ─── COIN EXCHANGE ────────────────────────────────────
    {
        "id": "coin_exchange",
        "name": "Coin Exchange — Cambio de Monedas",
        "type": "A",
        "topic": "voraz",
        "enunciado": """Implementa el algoritmo greedy de cambio de monedas del profesor.

FUNCIÓN REQUERIDA:
  money_exchange(value, coins) → lista con cantidad de cada moneda usada

EJEMPLO:
  coins = [500,200,100,50,20,10,5,2,1,0.5,0.2,0.1,0.05,0.02,0.01]
  money_exchange(4.57, coins) → [0,0,0,0,0,0,0,2,0,1,0,1,1,1,0]
  (2 monedas de 2, 1 de 0.5, 1 de 0.1, 1 de 0.05, 1 de 0.02)

NOTAS:
  • Usa división entera (//) y módulo (%) en cada iteración
  • Recorre las monedas de mayor a menor
  • Para con la lista de monedas agotada o value=0""",
        "prof_code": """def money_exchange(value, coins):
    exchange = [0] * len(coins)
    i = 0
    while i < len(coins) and value >= 0:
        exchange[i] = value // coins[i]
        value = value % coins[i]
        i += 1
    return exchange""",
        "test_cases": [
            {
                "setup": "coins = [500,200,100,50,20,10,5,2,1]",
                "call": "result = money_exchange(87, coins)",
                "restore": "",
                "check": "result[3] == 1 and result[4] == 1 and result[7] == 1 and result[8] == 2",
                "description": "87€ → 1x50 + 1x20 + 1x2·... correcta descomposición",
            },
            {
                "setup": "coins = [10, 5, 1]",
                "call": "result = money_exchange(27, coins)",
                "restore": "",
                "check": "result[0] == 2 and result[1] == 1 and result[2] == 2",
                "description": "27 con [10,5,1] → 2x10 + 1x5 + 2x1",
            },
        ],
    },
    # ─── TOPSORT ──────────────────────────────────────────
    {
        "id": "topsort",
        "name": "TopSort — Ordenación Topológica (DFS)",
        "type": "A",
        "topic": "grafos",
        "enunciado": """Implementa el algoritmo de ordenación topológica del profesor usando DFS.
El grafo es un diccionario de adyacencia.

FUNCIONES REQUERIDAS:
  topsort(g)           → inicializa datos y llama top_sort_visit para cada nodo
  top_sort_visit(data, k) → DFS que añade k al FRENTE de la lista al terminar

ESTRUCTURA data:
  {"graph": g, "state": {}, "d": {}, "f": {}, "time": 0, "list": deque()}

EJEMPLO:
  g = {"calcetines":["zapatos"], "pantalon":["zapatos","cinturon"],
       "camisa":["cinturon","jersey"], "zapatos":[], "cinturon":[], "jersey":[]}
  topsort(g)  → deque con orden topológico válido

NOTAS:
  • appendleft() al terminar un nodo (no append)
  • Estados: NOT_VISITED → VISITED → FINISHED""",
        "prof_code": """from collections import deque

def topsort(g):
    data = {
        "graph": g, "state": dict(), "d": dict(),
        "f": dict(), "time": 0, "list": deque()
    }
    for k in g.keys():
        data['state'][k] = 'NOT_VISITED'
        data['d'][k] = 0
        data['f'][k] = 0
    for k in g.keys():
        if data['state'][k] == "NOT_VISITED":
            top_sort_visit(data, k)
    print(data['list'])

def top_sort_visit(data, k):
    data['state'][k] = "VISITED"
    data['time'] += 1
    data['d'][k] = data['time']
    for adj in data['graph'][k]:
        if data['state'][adj] == "NOT_VISITED":
            top_sort_visit(data, adj)
    data['state'][k] = 'FINISHED'
    data['time'] += 1
    data['f'][k] = data['time']
    data['list'].appendleft(k)""",
        "test_cases": [
            {
                "setup": """
from collections import deque
g = {"A": ["B", "C"], "B": ["C"], "C": []}
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": "topsort(g)",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "'A' in captured.getvalue() and captured.getvalue().index('A') < captured.getvalue().index('C')",
                "description": "A debe aparecer antes que C en el orden topológico",
            },
        ],
    },
    # ─── LEXICAL TOPSORT ──────────────────────────────────
    {
        "id": "lexical_topsort",
        "name": "Lexical TopSort — Ordenación Topológica Lexicográfica",
        "type": "A",
        "topic": "grafos",
        "enunciado": """Implementa el TopSort lexicográfico del profesor (algoritmo de Kahn con orden léxico).

FUNCIÓN REQUERIDA:
  lexic_top_sort(g, n) → imprime orden topológico o -1 si hay ciclo

ALGORITMO:
  1. Cuenta aristas entrantes de cada nodo
  2. Añade a lista_inicial los nodos con 0 aristas entrantes
  3. En cada iteración: ORDENA la lista, saca el primero (menor), procesa vecinos
  4. Si cnt != n → hay ciclo → imprime -1

EJEMPLO (entrada estándar):
  n=5, m=6
  0 2 / 2 4 / 0 1 / 1 2 / 0 4 / 2 3
  Salida: 0 1 2 3 4

NOTAS:
  • Lee con: n, m = map(int, input().split())
  • Lee aristas: orig, dest = map(int, input().split())
  • La lista se ordena en cada iteración (no una vez)""",
        "prof_code": """def lexic_top_sort(g, n):
    aristas_entrantes = [0] * n
    for u in range(n):
        for v in g[u]:
            aristas_entrantes[v] += 1
    nodos_iniciales = []
    for i in range(n):
        if aristas_entrantes[i] == 0:
            nodos_iniciales.append(i)
    topological_sort = []
    cnt = 0
    while nodos_iniciales:
        nodos_iniciales.sort()
        origen = nodos_iniciales.pop(0)
        topological_sort.append(origen)
        for adj in g[origen]:
            aristas_entrantes[adj] -= 1
            if aristas_entrantes[adj] == 0:
                nodos_iniciales.append(adj)
        cnt += 1
    if cnt != n:
        print(-1)
        return
    for tarea in topological_sort:
        print(tarea, end=' ')

if __name__ == '__main__':
    n, m = map(int, input().strip().split())
    g = [[] for _ in range(n)]
    for _ in range(m):
        orig, dest = map(int, input().strip().split())
        g[orig].append(dest)
    lexic_top_sort(g, n)""",
        "test_cases": [
            {
                "setup": """
n = 5
g = [[] for _ in range(n)]
edges = [(0,2),(2,4),(0,1),(1,2),(0,4),(2,3)]
for o,d in edges: g[o].append(d)
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": "lexic_top_sort(g, n)",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "captured.getvalue().strip() == '0 1 2 3 4'",
                "description": "Orden lexicográfico: 0 1 2 3 4",
            },
        ],
    },
    # ─── TIPO B: La Velada (Scheduling) ──────────────────
    {
        "id": "b_velada",
        "name": "Road to La Velada — Scheduling de Actividades",
        "type": "B",
        "topic": "voraz",
        "enunciado": """PROBLEMA TIPO B — Procesa la entrada y aplica el algoritmo correcto.

Un streamer quiere hacer el máximo número de actividades sin que se solapen.
Implementa el algoritmo de selección de actividades por tiempo de fin más temprano.

ENTRADA A PROCESAR (simúlala en tu código):
  5
  Vacunarse 20 30
  BaniarAlPez 35 40
  Entrenar 31 60
  PonerTweets 10 15
  LlamadaConIbai 80 100

SALIDA ESPERADA:
  4

PISTAS:
  • Lee N actividades con nombre, inicio y fin
  • Ordena por tiempo de FIN (greedy clásico)
  • Selecciona si inicio >= fin_de_la_última_seleccionada
  • Imprime el total de actividades seleccionadas

Al final de tu código añade:
  # ALGORITMO USADO: nombre_del_algoritmo""",
        "prof_code": """# Solución de referencia del profesor
# Greedy scheduling por tiempo de fin más temprano
n = 5
actividades_raw = [
    ("Vacunarse", 20, 30),
    ("BaniarAlPez", 35, 40),
    ("Entrenar", 31, 60),
    ("PonerTweets", 10, 15),
    ("LlamadaConIbai", 80, 100),
]
actividades = sorted(actividades_raw, key=lambda x: x[2])
count = 0
last_end = -1
for nombre, inicio, fin in actividades:
    if inicio >= last_end:
        count += 1
        last_end = fin
print(count)
# ALGORITMO USADO: greedy_schedule (selección de actividades)""",
        "test_cases": [
            {
                "setup": """
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": """
n = 5
actividades_raw = [("Vacunarse",20,30),("BaniarAlPez",35,40),
                   ("Entrenar",31,60),("PonerTweets",10,15),("LlamadaConIbai",80,100)]
actividades = sorted(actividades_raw, key=lambda x: x[2])
count = 0; last_end = -1
for nombre, inicio, fin in actividades:
    if inicio >= last_end:
        count += 1; last_end = fin
print(count)
""",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "captured.getvalue().strip() == '4'",
                "description": "Máximo 4 actividades sin solapamiento",
            },
        ],
    },
    # ─── TIPO B: Dora la Examinadora (PARCIAL REAL) ──────
    {
        "id": "b_examinadora",
        "name": "Dora la Examinadora — Job Scheduling (PARCIAL REAL)",
        "type": "B",
        "topic": "voraz",
        "enunciado": """PROBLEMA TIPO B — Procesa la entrada y aplica el algoritmo correcto.
★ ESTE PROBLEMA SALIÓ EN EL PARCIAL REAL ★

Asigna autoescuelas a días de examen para maximizar el número de estudiantes examinados.
Cada autoescuela tiene: nombre, número de estudiantes y día máximo disponible.

ENTRADA A PROCESAR:
  4
  Julie_Evans 37 2
  Harrison_Mceachern 88 1
  Kendra_Walsh 48 0
  Maria_Hossack 98 3

SALIDA ESPERADA:
  271
  0: Kendra_Walsh
  1: Harrison_Mceachern
  2: Julie_Evans
  3: Maria_Hossack

ALGORITMO: Job Scheduling (greedy por beneficio, asigna al slot más tardío posible)

Al final de tu código añade:
  # ALGORITMO USADO: nombre_del_algoritmo""",
        "prof_code": """# Solución de referencia — Dora la Examinadora
n = 4
autoescuelas = [
    ("Julie_Evans", 37, 2),
    ("Harrison_Mceachern", 88, 1),
    ("Kendra_Walsh", 48, 0),
    ("Maria_Hossack", 98, 3),
]
autoescuelas.sort(key=lambda x: -x[1])
last_date = max(d for _,_,d in autoescuelas)
sol = {i: None for i in range(last_date+1)}
total = 0
for nombre, estudiantes, dia in autoescuelas:
    i = dia
    while i >= 0:
        if sol[i] is None:
            sol[i] = (nombre, estudiantes)
            total += estudiantes
            break
        i -= 1
print(total)
for i in range(last_date+1):
    if sol[i]:
        print(f"{i}: {sol[i][0]}")
# ALGORITMO USADO: greedy_schedule (job scheduling por beneficio)""",
        "test_cases": [
            {
                "setup": """
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": """
autoescuelas = [("Julie_Evans",37,2),("Harrison_Mceachern",88,1),
                ("Kendra_Walsh",48,0),("Maria_Hossack",98,3)]
autoescuelas.sort(key=lambda x: -x[1])
last_date = max(d for _,_,d in autoescuelas)
sol = {i: None for i in range(last_date+1)}
total = 0
for nombre, estudiantes, dia in autoescuelas:
    i = dia
    while i >= 0:
        if sol[i] is None:
            sol[i] = (nombre, estudiantes); total += estudiantes; break
        i -= 1
print(total)
""",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "captured.getvalue().strip().split()[0] == '271'",
                "description": "Total estudiantes examinados: 271",
            },
        ],
    },
    # ─── TIPO B: Fragmentos de Fortnite (PARCIAL REAL) ───
    {
        "id": "b_fortnite",
        "name": "Fragmentos de Fortnite — Kruskal MST (PARCIAL REAL)",
        "type": "B",
        "topic": "grafos",
        "enunciado": """PROBLEMA TIPO B — Procesa la entrada y aplica el algoritmo correcto.
★ ESTE PROBLEMA SALIÓ EN EL PARCIAL REAL ★

Encuentra la red de transporte de menor coste que conecte todos los fragmentos.
Además, guarda las conexiones de cada fragmento en el MST.

ENTRADA A PROCESAR:
  4 5
  0 1 3
  0 2 5
  1 2 1
  1 3 4
  2 3 2

SALIDA ESPERADA:
  6
  1 - 2
  2 - 3
  0 - 1
  [conexiones de cada fragmento en el MST]

ALGORITMO: Kruskal (MST)

Al final de tu código añade:
  # ALGORITMO USADO: nombre_del_algoritmo""",
        "prof_code": """# Solución de referencia — Fragmentos de Fortnite
n, m = 4, 5
aristas = [(3,0,1),(5,0,2),(1,1,2),(4,1,3),(2,2,3)]
aristas.sort()
comp = list(range(n))
def find(x):
    while comp[x] != x: x = comp[x]
    return x
sol = 0
elegidas = []
for w, u, v in aristas:
    ru, rv = find(u), find(v)
    if ru != rv:
        sol += w
        elegidas.append((min(u,v), max(u,v), w))
        comp[ru] = rv
elegidas.sort(key=lambda x: x[2])
print(sol)
for u,v,w in elegidas:
    print(f"{u} - {v}")
# ALGORITMO USADO: kruskal""",
        "test_cases": [
            {
                "setup": """
import io, sys
captured = io.StringIO()
sys.stdout = captured
""",
                "call": """
aristas = [(3,0,1),(5,0,2),(1,1,2),(4,1,3),(2,2,3)]
aristas.sort()
comp = list(range(4))
def find(x):
    while comp[x] != x: x = comp[x]
    return x
sol = 0
for w,u,v in aristas:
    ru,rv = find(u),find(v)
    if ru != rv:
        sol += w; comp[ru] = rv
print(sol)
""",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "captured.getvalue().strip() == '6'",
                "description": "MST de 4 nodos con esas aristas → coste 6",
            },
        ],
    },
    # ─── TIPO B: De ruta por París (PARCIAL REAL) ────────
    {
        "id": "b_paris",
        "name": "De Ruta por París — Dijkstra (PARCIAL REAL)",
        "type": "B",
        "topic": "grafos",
        "enunciado": """PROBLEMA TIPO B — Procesa la entrada y aplica el algoritmo correcto.
★ ESTE PROBLEMA SALIÓ EN EL PARCIAL REAL ★

Encontrar la ruta desde el hotel que, siguiendo el camino más corto,
visita el mayor número de lugares posible.

ENTRADA A PROCESAR:
  5 6 0
  0 1 10
  0 2 20
  1 3 5
  2 3 15
  3 4 10
  1 4 30

SALIDA ESPERADA:
  La distancia total + los nodos visitados en orden desde el hotel

ALGORITMO: Dijkstra desde el hotel

Al final de tu código añade:
  # ALGORITMO USADO: nombre_del_algoritmo""",
        "prof_code": """# Solución de referencia — De ruta por París
# Dijkstra + reconstrucción del camino de más nodos
INF = 0x3f3f3f3f
n, m, hotel = 5, 6, 0
grafo = [[] for _ in range(n)]
aristas = [(0,1,10),(0,2,20),(1,3,5),(2,3,15),(3,4,10),(1,4,30)]
for u,v,w in aristas:
    grafo[u].append((u,v,w))
    grafo[v].append((v,u,w))
dist = [INF]*n
dist[hotel] = 0
prev = [-1]*n
visited = [False]*n
for _ in range(n):
    u = min((dist[i],i) for i in range(n) if not visited[i])[1]
    visited[u] = True
    for src,dst,w in grafo[u]:
        if dist[u]+w < dist[dst]:
            dist[dst] = dist[u]+w
            prev[dst] = u
# reconstruir camino al nodo más lejano alcanzable
destino = max(range(n), key=lambda x: (dist[x]<INF, -dist[x]))
path = []
cur = destino
while cur != -1:
    path.append(cur)
    cur = prev[cur]
path.reverse()
print(dist[destino])
print(*path)
# ALGORITMO USADO: dijkstra""",
        "test_cases": [
            {
                "setup": """
INF = 0x3f3f3f3f
n, hotel = 5, 0
grafo = [[] for _ in range(n)]
for u,v,w in [(0,1,10),(0,2,20),(1,3,5),(2,3,15),(3,4,10),(1,4,30)]:
    grafo[u].append((u,v,w)); grafo[v].append((v,u,w))
dist = [INF]*n; dist[hotel]=0; visited=[False]*n
for _ in range(n):
    u = min((dist[i],i) for i in range(n) if not visited[i])[1]
    visited[u]=True
    for src,dst,w in grafo[u]:
        if dist[u]+w<dist[dst]: dist[dst]=dist[u]+w
""",
                "call": "result = dist",
                "restore": "",
                "check": "result[1] == 10 and result[3] == 15 and result[4] == 25",
                "description": "Dijkstra desde 0: dist[1]=10, dist[3]=15, dist[4]=25",
            },
        ],
    },
]


QUESTIONS_P2 = [
    # ─── MERGE SORT ──────────────────────────────────────
    {
        "id": "merge_sort",
        "name": "Merge Sort — Ordenación por Mezcla",
        "type": "A",
        "topic": "dyv",
        "enunciado": """Implementa el algoritmo Merge Sort del profesor (Divide y Vencerás).

FUNCIONES REQUERIDAS:
  merge(left, right, v)   → combina dos mitades ordenadas en v (in-place)
  merge_sort(v)           → divide recursivamente y llama a merge

EJEMPLO:
  v = [3, 1, 4, 1, 7, 9, 2, 6, 5, 3, 5, 8]
  merge_sort(v)
  print(v)  → [1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9]

NOTAS:
  • merge recibe left y right como COPIAS, no vistas
  • Modifica v in-place (no devuelve nada)
  • Caso base: len(v) == 1
  • mid = len(v) // 2""",
        "prof_code": """def merge(left, right, v):
    l = 0; r = 0; i = 0
    while l < len(left) and r < len(right):
        if left[l] <= right[r]:
            v[i] = left[l]; l += 1
        else:
            v[i] = right[r]; r += 1
        i += 1
    if r == len(right):
        f = l; resto = left
    else:
        f = r; resto = right
    for j in range(f, len(resto)):
        v[i] = resto[j]; i += 1

def merge_sort(v):
    if len(v) == 1:
        return
    else:
        mid = len(v) // 2
        left = v[:mid]
        right = v[mid:]
        merge_sort(left)
        merge_sort(right)
        merge(left, right, v)""",
        "test_cases": [
            {
                "setup": "v = [3, 1, 4, 1, 7, 9, 2, 6, 5, 3, 5, 8]",
                "call": "merge_sort(v)",
                "restore": "",
                "check": "v == [1, 1, 2, 3, 3, 4, 5, 5, 6, 7, 8, 9]",
                "description": "Ordena [3,1,4,1,7,9,2,6,5,3,5,8]",
            },
            {
                "setup": "v = [5, 2, 8, 1, 9, 3]",
                "call": "merge_sort(v)",
                "restore": "",
                "check": "v == [1, 2, 3, 5, 8, 9]",
                "description": "Ordena [5,2,8,1,9,3]",
            },
            {
                "setup": "v = [1]",
                "call": "merge_sort(v)",
                "restore": "",
                "check": "v == [1]",
                "description": "Lista de un elemento no cambia",
            },
        ],
    },
    # ─── QUICK SORT ──────────────────────────────────────
    {
        "id": "quicksort",
        "name": "Quick Sort — Ordenación Rápida",
        "type": "A",
        "topic": "dyv",
        "enunciado": """Implementa el algoritmo Quick Sort del profesor.

FUNCIONES REQUERIDAS:
  pivot(v, left, right) → particiona v entre [left..right] en torno a v[left]
                          devuelve la posición final del pivote
  quick_sort(v, i, j)   → ordena v[i..j] recursivamente

EJEMPLO:
  v = [9, 4, 17, 21, 34, 6, 0, -5, 56, 14, 8, 43]
  quick_sort(v, 0, len(v)-1)
  print(v)  → [-5, 0, 4, 6, 8, 9, 14, 17, 21, 34, 43, 56]

NOTAS:
  • El pivote es SIEMPRE v[left]
  • La función pivot mueve elementos y devuelve la posición final del pivote
  • Caso base: i > j (no i >= j)""",
        "prof_code": """def pivot(v, left, right):
    pivote = v[left]
    i = left+1
    while i < right and v[i] < pivote:
        i += 1
    j = right
    while j > left and v[j] > pivote:
        j -= 1
    while i < j:
        v[i], v[j] = v[j], v[i]
        i += 1
        while v[i] < pivote:
            i += 1
        j -= 1
        while v[j] > pivote:
            j -= 1
    v[left], v[j] = v[j], v[left]
    return j

def quick_sort(v, i, j):
    if i > j:
        return
    else:
        pivote = pivot(v, i, j)
        quick_sort(v, i, pivote - 1)
        quick_sort(v, pivote + 1, j)""",
        "test_cases": [
            {
                "setup": "v = [9, 4, 17, 21, 34, 6, 0, -5, 56, 14, 8, 43]",
                "call": "quick_sort(v, 0, len(v)-1)",
                "restore": "",
                "check": "v == [-5, 0, 4, 6, 8, 9, 14, 17, 21, 34, 43, 56]",
                "description": "Ordena lista de 12 elementos con negativos",
            },
            {
                "setup": "v = [3, 1, 2]",
                "call": "quick_sort(v, 0, 2)",
                "restore": "",
                "check": "v == [1, 2, 3]",
                "description": "Ordena [3,1,2]",
            },
        ],
    },
    # ─── BINARY SEARCH RECURSIVO ─────────────────────────
    {
        "id": "binary_search",
        "name": "Binary Search Recursivo",
        "type": "A",
        "topic": "dyv",
        "enunciado": """Implementa la búsqueda binaria RECURSIVA del profesor.

FUNCIÓN REQUERIDA:
  binary_search(v, number, low, high)
  → devuelve índice si encuentra number en v
  → devuelve low si no encuentra (posición donde iría)

EJEMPLO:
  v = [1, 3, 3, 5, 6, 7, 9]
  binary_search(v, 6, 0, 6) → 4   (encontrado en índice 4)
  binary_search(v, 0, 0, 6) → 0   (no encontrado, iría en posición 0)
  binary_search(v, 4, 0, 6) → 3   (no encontrado, iría en posición 3)

NOTAS:
  • Caso base: low > high → return low
  • mid = (low + high) // 2
  • Si number < v[mid] → busca en [low, mid-1]
  • Si number > v[mid] → busca en [mid+1, high]""",
        "prof_code": """def binary_search(v, number, low, high):
    if low > high:
        return low
    else:
        mid = (low + high) // 2
        if number == v[mid]:
            return mid
        if number < v[mid]:
            return binary_search(v, number, low, mid-1)
        else:
            return binary_search(v, number, mid+1, high)""",
        "test_cases": [
            {
                "setup": "v = [1, 3, 3, 5, 6, 7, 9]",
                "call": "result = binary_search(v, 6, 0, len(v)-1)",
                "restore": "",
                "check": "result == 4",
                "description": "Encontrar 6 en v → índice 4",
            },
            {
                "setup": "v = [1, 3, 5, 7, 9]",
                "call": "result = binary_search(v, 5, 0, len(v)-1)",
                "restore": "",
                "check": "result == 2",
                "description": "Encontrar 5 en [1,3,5,7,9] → índice 2",
            },
            {
                "setup": "v = [1, 3, 5, 7, 9]",
                "call": "result = binary_search(v, 4, 0, len(v)-1)",
                "restore": "",
                "check": "result == 2",
                "description": "4 no existe, iría en posición 2 (entre 3 y 5)",
            },
        ],
    },
    # ─── BINARY SEARCH ITERATIVO ─────────────────────────
    {
        "id": "binary_search_iter",
        "name": "Binary Search Iterativo",
        "type": "A",
        "topic": "dyv",
        "enunciado": """Implementa la búsqueda binaria ITERATIVA del profesor.

FUNCIÓN REQUERIDA:
  binary_search(v, number)
  → devuelve índice si encuentra
  → devuelve -low si no encuentra (valor negativo)

EJEMPLO:
  v = [1, 3, 3, 5, 6, 7, 9]
  binary_search(v, 6) → 4    (encontrado)
  binary_search(v, 0) → 0    (no encontrado, -low = -(0) = 0... retorna -low)
  binary_search(v, 4) → -3   (no encontrado, low=3 al salir → retorna -3)

NOTAS:
  • Usa while low <= high
  • Al salir sin encontrar: return -low
  • A diferencia del recursivo, solo recibe v y number (no low/high)""",
        "prof_code": """def binary_search(v, number):
    low = 0
    high = len(v) - 1
    while low <= high:
        mid = (low + high) // 2
        if number == v[mid]:
            return mid
        if number < v[mid]:
            high = mid-1
        else:
            low = mid+1
    return -low""",
        "test_cases": [
            {
                "setup": "v = [1, 3, 3, 5, 6, 7, 9]",
                "call": "result = binary_search(v, 6)",
                "restore": "",
                "check": "result == 4",
                "description": "Encontrar 6 → índice 4",
            },
            {
                "setup": "v = [1, 3, 5, 7, 9]",
                "call": "result = binary_search(v, 4)",
                "restore": "",
                "check": "result < 0",
                "description": "4 no existe → retorna valor negativo",
            },
        ],
    },
    # ─── MAX VECTOR ──────────────────────────────────────
    {
        "id": "max_vector",
        "name": "Max Vector — Divide y Vencerás",
        "type": "A",
        "topic": "dyv",
        "enunciado": """Implementa las 3 versiones de max_vector del profesor.

FUNCIONES REQUERIDAS:
  max_vector_trad(v)              → máximo iterativo clásico
  max_vector_dyv(v)               → DyV con slicing (v[:mid] y v[mid:])
  max_vector_dyv_efficient(v,l,h) → DyV con índices l y h (sin copias)

EJEMPLO:
  v = [3, 1, 9, 2, 7, 4]
  max_vector_trad(v)              → 9
  max_vector_dyv(v)               → 9
  max_vector_dyv_efficient(v,0,5) → 9

NOTAS:
  • max_vector_dyv: caso base len(v)==1 → llama max_vector_trad(v)
  • max_vector_dyv_efficient: caso base l==h → return v[l]
  • Ambas DyV usan mitad = (l+h)//2 o len(v)//2""",
        "prof_code": """def max_vector_trad(v):
    m = v[0]
    for i in range(1, len(v)):
        m = max(m, v[i])
    return m

def max_vector_dyv(v):
    if len(v) == 1:
        return max_vector_trad(v)
    else:
        mitad = len(v) // 2
        izq = max_vector_dyv(v[0:mitad])
        der = max_vector_dyv(v[mitad:len(v)])
        return max(izq, der)

def max_vector_dyv_efficient(v, l, h):
    if l == h:
        return v[l]
    else:
        mitad = (l + h) // 2
        izq = max_vector_dyv_efficient(v, l, mitad)
        der = max_vector_dyv_efficient(v, mitad+1, h)
        return max(izq, der)""",
        "test_cases": [
            {
                "setup": "v = [3, 1, 9, 2, 7, 4]",
                "call": "r1 = max_vector_trad(v); r2 = max_vector_dyv(v); r3 = max_vector_dyv_efficient(v, 0, len(v)-1)",
                "restore": "",
                "check": "r1 == 9 and r2 == 9 and r3 == 9",
                "description": "Las 3 versiones devuelven 9",
            },
            {
                "setup": "v = [5]",
                "call": "r = max_vector_dyv_efficient(v, 0, 0)",
                "restore": "",
                "check": "r == 5",
                "description": "Lista de un elemento",
            },
        ],
    },
    # ─── KNAPSACK BT ─────────────────────────────────────
    {
        "id": "knapsack_bt",
        "name": "Mochila BT — Backtracking (versión con 'o')",
        "type": "A",
        "topic": "backtracking",
        "enunciado": """Implementa la mochila por Backtracking del profesor (con campo 'o' en sol).

FUNCIONES REQUERIDAS:
  is_solution(sol, data)      → True si no cabe ningún objeto más
  is_feasible(sol, data, i)   → True si el objeto i cabe en la mochila
  add(sol, data, i)           → añade objeto i a la solución
  remove(sol, data, i)        → elimina objeto i de la solución
  knapsack_bt(data, sol, best_sol, k) → devuelve best_sol

EJEMPLO:
  data = {'n':4, 'W':8, 'w':[2,3,4,5], 'v':[3,5,6,10]}
  sol = {'o':[0]*4, 'v':0, 'w':0}
  best_sol = {'o':[0]*4, 'v':0, 'w':0}
  best_sol = knapsack_bt(data, sol, best_sol, 0)
  → best_sol['v'] == 13  (objetos 0+1+2: valor 3+5+6=14 o 1+3: 5+10=15...)

NOTAS:
  • is_solution: sol['w'] + min(data['w']) > data['W']
  • Usa copy.deepcopy(sol) para guardar best_sol
  • El tercer parámetro de knapsack_bt es el índice k (no usar i+1 como en la otra versión)""",
        "prof_code": """import copy

def is_solution(sol, data):
    return sol['w'] + min(data['w']) > data['W']

def is_feasible(sol, data, i):
    return sol['w'] + data['w'][i] <= data['W']

def add(sol, data, i):
    sol['o'][i] += 1
    sol['v'] += data['v'][i]
    sol['w'] += data['w'][i]

def remove(sol, data, i):
    sol['o'][i] -= 1
    sol['v'] -= data['v'][i]
    sol['w'] -= data['w'][i]

def knapsack_bt(data, sol, best_sol, k):
    if is_solution(sol, data):
        print(f"EXPLORADA -> {sol}")
        if sol['v'] > best_sol['v']:
            best_sol = copy.deepcopy(sol)
    else:
        for i in range(k, data['n']):
            if is_feasible(sol, data, i):
                add(sol, data, i)
                best_sol = knapsack_bt(data, sol, best_sol, i)
                remove(sol, data, i)
    return best_sol""",
        "test_cases": [
            {
                "setup": """
import copy
data = {'n':4, 'W':8, 'w':[2,3,4,5], 'v':[3,5,6,10]}
sol = {'o':[0]*4, 'v':0, 'w':0}
best_sol = {'o':[0]*4, 'v':0, 'w':0}
import io, sys
sys.stdout = io.StringIO()
""",
                "call": "best_sol = knapsack_bt(data, sol, best_sol, 0)",
                "restore": "sys.stdout = sys.__stdout__",
                "check": "best_sol['v'] >= 13",
                "description": "Valor óptimo ≥ 13 (p.ej. objetos 1+3: 5+10=15)",
            },
        ],
    },
    # ─── MOCHILA 0/1 ─────────────────────────────────────
    {
        "id": "mochila_01",
        "name": "Mochila 0/1 — Backtracking (versión con 'obj')",
        "type": "A",
        "topic": "backtracking",
        "enunciado": """Implementa la mochila 0/1 por BT del profesor (variante con 'obj' en sol).

FUNCIONES REQUERIDAS:
  init_data()                         → devuelve diccionario de datos
  init_sol(data)                      → devuelve {'obj':[0]*n, 'w':0, 'v':0}
  add(sol, data, i) / remove(sol, data, i)
  best(sol_1, sol_2)                  → deepcopy del mejor
  is_solution(sol, data) / is_feasible(sol, data, i)
  knapsack_0_1(data, sol, best_sol, k) → devuelve best_sol

DATA por defecto: n=4, W=8, w=[2,3,4,5], v=[3,5,6,10]

DIFERENCIA con knapsack_bt: usa i+1 en la llamada recursiva (no i),
y usa 'obj' en lugar de 'o', y best() para comparar soluciones.""",
        "prof_code": """import copy

def init_data():
    data = {}
    data['n'] = 4; data['W'] = 8
    data['w'] = [2,3,4,5]; data['v'] = [3,5,6,10]
    return data

def init_sol(data):
    sol = {}
    sol['obj'] = [0] * data['n']
    sol['w'] = 0; sol['v'] = 0
    return sol

def add(sol, data, i):
    sol['obj'][i] = 1
    sol['w'] += data['w'][i]; sol['v'] += data['v'][i]

def remove(sol, data, i):
    sol['obj'][i] = 0
    sol['w'] -= data['w'][i]; sol['v'] -= data['v'][i]

def best(sol_1, sol_2):
    if sol_1['v'] > sol_2['v']:
        return copy.deepcopy(sol_1)
    else:
        return copy.deepcopy(sol_2)

def is_solution(sol, data):
    return sol['w'] + min(data['w']) > data['W']

def is_feasible(sol, data, i):
    return sol['w'] + data['w'][i] <= data['W']

def knapsack_0_1(data, sol, best_sol, k):
    if is_solution(sol, data):
        best_sol = best(best_sol, sol)
    else:
        for i in range(k, data['n']):
            if is_feasible(sol, data, i):
                add(sol, data, i)
                best_sol = knapsack_0_1(data, sol, best_sol, i+1)
                remove(sol, data, i)
    return best_sol""",
        "test_cases": [
            {
                "setup": """
import copy
data = {'n':4,'W':8,'w':[2,3,4,5],'v':[3,5,6,10]}
sol = {'obj':[0]*4,'w':0,'v':0}
best_sol = {'obj':[0]*4,'w':0,'v':0}
""",
                "call": "best_sol = knapsack_0_1(data, sol, best_sol, 0)",
                "restore": "",
                "check": "best_sol['v'] >= 13",
                "description": "Valor óptimo ≥ 13",
            },
        ],
    },
    # ─── N-QUEENS UNA SOLUCIÓN ────────────────────────────
    {
        "id": "nqueens_one",
        "name": "N-Queens — Una Solución (Backtracking)",
        "type": "A",
        "topic": "backtracking",
        "enunciado": """Implementa N-Queens que encuentra UNA solución (del profesor).

FUNCIONES REQUERIDAS:
  is_sol(sol, row)              → True si row == len(sol)
  is_feasible(sol, row, col)    → True si la reina en (row,col) no ataca a ninguna anterior
  nqueens(sol, n, found, row)   → devuelve (sol, found)

EJEMPLO:
  n = 8
  sol = [-1]*8
  sol, found = nqueens(sol, n, False, 0)
  if found: print(sol)  → alguna configuración válida como [0,4,7,5,2,6,1,3]

NOTAS:
  • is_feasible usa while con i=1..row
  • Verifica columna, diagonal 45° y diagonal 135°
  • Cuando found=True deja de explorar (para en el primer encontrado)
  • sol[row] = -1 al hacer backtrack""",
        "prof_code": """def is_sol(sol, row):
    return row == len(sol)

def is_feasible(sol, row, col):
    is_feas = True; i = 1
    while is_feas and i <= row:
        feas_col = sol[row-i] == -1 or sol[row-i] != col
        feas_diag1 = sol[row-i] == -1 or col-i < 0 or sol[row-i] != col-i
        feas_diag2 = sol[row-i] == -1 or col+1 >= len(sol) or sol[row-i] != col+i
        is_feas = feas_col and feas_diag1 and feas_diag2; i += 1
    return is_feas

def nqueens(sol, n, found, row):
    if is_sol(sol, row):
        found = True
    else:
        col = 0
        while not found and col < n:
            if is_feasible(sol, row, col):
                sol[row] = col
                sol, found = nqueens(sol, n, found, row+1)
                if not found:
                    sol[row] = -1
            col += 1
    return sol, found""",
        "test_cases": [
            {
                "setup": "sol = [-1]*8; n = 8",
                "call": "sol, found = nqueens(sol, n, False, 0)",
                "restore": "",
                "check": "found == True and len(sol) == 8 and all(x != -1 for x in sol)",
                "description": "N=8: encuentra una solución válida",
            },
            {
                "setup": "sol = [-1]*4; n = 4",
                "call": "sol, found = nqueens(sol, n, False, 0)",
                "restore": "",
                "check": "found == True",
                "description": "N=4: encuentra solución",
            },
        ],
    },
    # ─── COLOREO GRAFOS ──────────────────────────────────
    {
        "id": "coloreado",
        "name": "Coloreo de Grafos — Una Solución",
        "type": "A",
        "topic": "backtracking",
        "enunciado": """Implementa el coloreo de grafos (una solución) del profesor.

FUNCIONES REQUERIDAS:
  init_graph()                     → {'n':4, 'g':[[1,2,3],[0],[0,3],[0,2]]}
  init_sol(g)                      → [0]*g['n']
  is_sol(g, node)                  → node == g['n']
  is_feasible(g, sol, node, color) → ningún adyacente ya coloreado tiene ese color
  coloring_va(g, m, sol, node)     → devuelve (sol, found)

EJEMPLO:
  g = init_graph()
  sol = init_sol(g)
  sol, found = coloring_va(g, 3, sol, 0)
  if found: print(sol)  → [1, 2, 2, 3] o similar

NOTAS:
  • is_feasible solo mira adyacentes con adj < node (ya coloreados)
  • Si no encuentra solución con m colores → devuelve (sol, False)
  • Backtrack: sol[node] = 0 si no encontrado""",
        "prof_code": """def init_graph():
    data = {}
    data['n'] = 4
    data['g'] = [[1,2,3], [0], [0,3], [0,2]]
    return data

def init_sol(g):
    sol = [0] * g['n']
    return sol

def is_sol(g, node):
    return node == g['n']

def is_feasible(g, sol, node, color):
    adj_list = g['g'][node]
    for adj in adj_list:
        if adj < node and sol[adj] == color:
            return False
    return True

def coloring_va(g, m, sol, node):
    if is_sol(g, node):
        found = True
    else:
        found = False; color = 1
        while not found and color <= m:
            if is_feasible(g, sol, node, color):
                sol[node] = color
                sol, found = coloring_va(g, m, sol, node+1)
                if not found:
                    sol[node] = 0
            color += 1
    return sol, found""",
        "test_cases": [
            {
                "setup": """
def _ig(): return {'n':4,'g':[[1,2,3],[0],[0,3],[0,2]]}
g = _ig(); sol = [0]*g['n']
""",
                "call": "sol, found = coloring_va(g, 3, sol, 0)",
                "restore": "",
                "check": "found == True and all(x > 0 for x in sol)",
                "description": "Grafo 4 nodos con 3 colores → encontrada",
            },
            {
                "setup": """
g = {'n':3,'g':[[1,2],[0,2],[0,1]]}; sol = [0]*3
""",
                "call": "sol, found = coloring_va(g, 2, sol, 0)",
                "restore": "",
                "check": "found == False",
                "description": "Triángulo completo no se puede colorear con 2 colores",
            },
        ],
    },
    # ─── TIPO B: Caos en la Biblioteca ───────────────────
    {
        "id": "b_caos_biblioteca",
        "name": "Caos en la Biblioteca — Inversiones con Merge Sort",
        "type": "B",
        "topic": "dyv",
        "enunciado": """PROBLEMA TIPO B — Procesa la entrada y aplica el algoritmo correcto.

Cuenta el número de inversiones en una lista (pares (i,j) donde i<j pero v[i]>v[j]).
Usa Merge Sort modificado para contar inversiones eficientemente.

ENTRADA A PROCESAR:
  1
  2 4 1 3 5

SALIDA ESPERADA:
  3
  3

(3 inversiones: (2,1), (4,1), (4,3) — luego suma total también 3)

PISTAS:
  • Lee N estanterías, para cada una lee la lista de series
  • Modifica merge para que cuente inversiones al mezclar
  • Al final imprime el grado de caos de cada estantería y la suma total

Al final de tu código:
  # ALGORITMO USADO: nombre_del_algoritmo""",
        "prof_code": """def merge_count(v):
    if len(v) <= 1:
        return v, 0
    mid = len(v) // 2
    left, cl = merge_count(v[:mid])
    right, cr = merge_count(v[mid:])
    merged = []; count = cl + cr; i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
            count += len(left) - i
    merged += left[i:]; merged += right[j:]
    return merged, count

n = int(input())
total = 0
for _ in range(n):
    v = list(map(int, input().split()))
    _, c = merge_count(v)
    print(c); total += c
print(total)
# ALGORITMO USADO: merge_sort (conteo de inversiones)""",
        "test_cases": [
            {
                "setup": """
def merge_count(v):
    if len(v)<=1: return v,0
    mid=len(v)//2
    left,cl=merge_count(v[:mid]); right,cr=merge_count(v[mid:])
    merged=[]; count=cl+cr; i=j=0
    while i<len(left) and j<len(right):
        if left[i]<=right[j]: merged.append(left[i]); i+=1
        else: merged.append(right[j]); j+=1; count+=len(left)-i
    merged+=left[i:]; merged+=right[j:]
    return merged,count
""",
                "call": "_, inversions = merge_count([2,4,1,3,5])",
                "restore": "",
                "check": "inversions == 3",
                "description": "Inversiones en [2,4,1,3,5] → 3",
            },
        ],
    },
    # ─── TIPO B: Clear Souls ─────────────────────────────
    {
        "id": "b_clearsouls",
        "name": "Clear Souls — Binary Search en Lista Ordenada",
        "type": "B",
        "topic": "dyv",
        "enunciado": """PROBLEMA TIPO B — Procesa la entrada y aplica el algoritmo correcto.

Dada una lista ORDENADA de niveles de enemigos, para cada consulta Q
encuentra cuántos enemigos tienen nivel ≤ Q y la suma de sus niveles.

ENTRADA A PROCESAR:
  7
  1 2 3 4 5 6 7
  3
  3
  10
  2

SALIDA ESPERADA:
  3 6
  7 28
  2 3

PISTAS:
  • La lista está ordenada → usa búsqueda binaria
  • Precalcula prefix sums para la suma eficiente
  • Para Q=3: hay 3 enemigos (1,2,3), suma=6
  • Para Q=10: todos los 7, suma=28

Al final de tu código:
  # ALGORITMO USADO: nombre_del_algoritmo""",
        "prof_code": """def binary_search(v, q):
    low = 0; high = len(v)-1; pos = -1
    while low <= high:
        mid = (low+high)//2
        if v[mid] <= q: pos = mid; low = mid+1
        else: high = mid-1
    return pos

n = int(input())
v = list(map(int, input().split()))
prefix = [0]*(n+1)
for i in range(n): prefix[i+1] = prefix[i]+v[i]
m = int(input())
for _ in range(m):
    q = int(input())
    pos = binary_search(v, q)
    if pos == -1: print(0, 0)
    else: print(pos+1, prefix[pos+1])
# ALGORITMO USADO: binary_search""",
        "test_cases": [
            {
                "setup": """
def bs(v,q):
    low=0;high=len(v)-1;pos=-1
    while low<=high:
        mid=(low+high)//2
        if v[mid]<=q: pos=mid;low=mid+1
        else: high=mid-1
    return pos
v=[1,2,3,4,5,6,7]
prefix=[0]*8
for i in range(7): prefix[i+1]=prefix[i]+v[i]
""",
                "call": "pos3=bs(v,3); pos10=bs(v,10); res3=(pos3+1,prefix[pos3+1]); res10=(pos10+1,prefix[pos10+1])",
                "restore": "",
                "check": "res3 == (3,6) and res10 == (7,28)",
                "description": "Q=3→(3,6), Q=10→(7,28)",
            },
        ],
    },
]
