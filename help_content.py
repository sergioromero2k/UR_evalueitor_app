HELP_CONTENT = {
    "BFS — Búsqueda en Anchura": {
        "color": "#00aaff",
        "keywords": ["nivel a nivel", "más cercano primero", "camino más corto sin pesos", "componentes conexos", "recorrer grafo"],
        "cuando": "Cuando necesitas explorar por niveles o encontrar el camino más corto en un grafo SIN pesos.",
        "truco": "¿Te piden visitar nodos nivel a nivel? ¿Camino mínimo sin pesos? → BFS",
        "funcion": "bfs(g)",
        "estructura": "Cola (deque), visited como lista o set"
    },
    "DFS — Búsqueda en Profundidad": {
        "color": "#00aaff",
        "keywords": ["profundidad", "explorar hasta el fondo", "componentes", "ciclos", "backtracking base"],
        "cuando": "Cuando necesitas explorar un camino hasta el fondo antes de probar otro.",
        "truco": "¿Te piden orden de exploración en profundidad? ¿Detectar ciclos? → DFS",
        "funcion": "dfs(g)",
        "estructura": "Pila implícita (recursión), visited como set"
    },
    "Dijkstra — Caminos Mínimos": {
        "color": "#00aaff",
        "keywords": ["camino más corto", "distancia mínima", "grafo con pesos", "GPS", "ruta óptima"],
        "cuando": "Cuando el grafo tiene PESOS y necesitas la distancia mínima desde un nodo origen.",
        "truco": "¿Hay pesos en las aristas? ¿Distancia mínima desde un punto? → DIJKSTRA",
        "funcion": "dijkstra(g, start)",
        "estructura": "distances[], visited[], select_min()"
    },
    "Prim — MST": {
        "color": "#00aaff",
        "keywords": ["árbol expansión mínima", "conectar todos", "menor coste total", "MST", "red mínima"],
        "cuando": "Cuando necesitas conectar todos los nodos con el mínimo coste total (MST). Crece desde un nodo.",
        "truco": "¿Conectar todos con mínimo coste? ¿Crece desde un nodo? → PRIM",
        "funcion": "prim(g)",
        "estructura": "candidates[], visited[], select_min()"
    },
    "Kruskal — MST": {
        "color": "#00aaff",
        "keywords": ["árbol expansión mínima", "MST", "ordenar aristas", "componentes", "menor coste"],
        "cuando": "Igual que Prim pero ordena todas las aristas primero. Usa componentes para evitar ciclos.",
        "truco": "¿MST? ¿Te dan lista de aristas? → KRUSKAL. Diferencia con Prim: Kruskal ordena aristas, Prim crece desde nodo.",
        "funcion": "kruskal(g)",
        "estructura": "sort_candidates(), components[], update_components()"
    },
    "TopSort — Ordenación Topológica": {
        "color": "#00aaff",
        "keywords": ["orden de tareas", "prerequisitos", "dependencias", "DAG", "orden válido"],
        "cuando": "Cuando hay dependencias entre tareas y necesitas un orden válido para hacerlas.",
        "truco": "¿Tarea A debe hacerse antes que B? ¿Orden de cursos? → TOPSORT",
        "funcion": "topsort(g)",
        "estructura": "DFS + appendleft al terminar cada nodo"
    },
    "Lexical TopSort — TopSort Lexicográfico": {
        "color": "#00aaff",
        "keywords": ["orden topológico", "lexicográfico", "menor identificador primero", "Kahn", "ciclo → -1"],
        "cuando": "Igual que TopSort pero cuando hay empate siempre elige el nodo de menor identificador.",
        "truco": "¿TopSort con orden lexicográfico? ¿Detectar ciclos (-1)? → LEXICAL TOPSORT",
        "funcion": "lexic_top_sort(g, n)",
        "estructura": "aristas_entrantes[], nodos_iniciales.sort()"
    },
    "Scheduling — Maximizar Beneficio": {
        "color": "#ff8c00",
        "keywords": ["maximizar beneficio", "deadline", "fecha límite", "seleccionar tareas", "slot de tiempo"],
        "cuando": "Cuando debes ELEGIR qué tareas hacer para maximizar el beneficio, cada una con un deadline.",
        "truco": "¿Elegir cuáles hacer? ¿Maximizar ganancia con fechas límite? → SCHEDULING",
        "funcion": "greedy_schedule(names, profit, deadline)",
        "estructura": "Ordenar por beneficio desc, asignar al slot más tardío libre"
    },
    "Waiting Time — Minimizar Espera": {
        "color": "#ff8c00",
        "keywords": ["minimizar espera", "todos se atienden", "orden óptimo", "tiempo total", "cola"],
        "cuando": "Cuando TODOS deben ser atendidos y quieres minimizar el tiempo de espera total.",
        "truco": "¿Todos se atienden? ¿Minimizar espera total? → WAITING TIME. Ordena por duración ascendente.",
        "funcion": "order_tasks(names, tasks)",
        "estructura": "Ordenar por duración ascendente (el más corto primero)"
    },
    "Coin Exchange — Cambio de Monedas": {
        "color": "#ff8c00",
        "keywords": ["cambio", "monedas", "devolver", "menor número de monedas", "divisas"],
        "cuando": "Cuando debes devolver un valor usando el menor número de monedas posible.",
        "truco": "¿Devolver cambio con monedas? → COIN EXCHANGE. Siempre coge la moneda más grande posible.",
        "funcion": "money_exchange(value, coins)",
        "estructura": "coins ordenadas desc, value // coin en cada paso"
    },
    "Greedy Knapsack — Mochila Fraccionable": {
        "color": "#ff8c00",
        "keywords": ["mochila", "fracción", "ratio valor/peso", "maximizar valor", "se puede dividir"],
        "cuando": "Mochila donde SÍ puedes llevarte fracciones de objetos. Ordena por ratio valor/peso.",
        "truco": "¿Mochila con fracciones permitidas? → GREEDY KNAPSACK. ¿Sin fracciones? → BT",
        "funcion": "greedy_knapsack(v, w, W)",
        "estructura": "Ordenar por ratio v/w desc, llevar fracción si no cabe entero"
    },
    "Art Points — Puntos de Articulación": {
        "color": "#00aaff",
        "keywords": ["servidor crítico", "punto de articulación", "desconecta la red", "nodo crítico", "eliminar nodo"],
        "cuando": "Cuando necesitas encontrar qué nodos, si se eliminan, desconectan la red.",
        "truco": "¿Qué nodo es crítico para la conectividad? → ART POINTS",
        "funcion": "findArticulationPoints(g)",
        "estructura": "DFS + disc[], low[], parent[], ap[]"
    },
    "Merge Sort — Ordenación por Mezcla": {
        "color": "#aa00ff",
        "keywords": ["ordenar", "dividir y vencer", "mezcla", "mitades", "O(n log n)"],
        "cuando": "Ordenación estable y eficiente. Divide en mitades, ordena cada una y mezcla.",
        "truco": "¿Ordenar con DyV? → MERGE SORT. También sirve para contar inversiones.",
        "funcion": "merge_sort(v)",
        "estructura": "Divide en left/right, merge() combina in-place"
    },
    "Quick Sort — Ordenación Rápida": {
        "color": "#aa00ff",
        "keywords": ["ordenar", "pivote", "partición", "in-place", "rápido"],
        "cuando": "Ordenación rápida in-place. Elige un pivote y particiona.",
        "truco": "¿Ordenar con pivote? → QUICK SORT. Pivote siempre es v[left] en el código del profesor.",
        "funcion": "quick_sort(v, i, j)",
        "estructura": "pivot() particiona, llamadas recursivas a cada partición"
    },
    "Binary Search — Búsqueda Binaria": {
        "color": "#aa00ff",
        "keywords": ["buscar en lista ordenada", "posición", "O(log n)", "dividir a la mitad", "catálogo ordenado"],
        "cuando": "Cuando la lista está ORDENADA y necesitas encontrar un elemento rápidamente.",
        "truco": "¿Lista ordenada? ¿Buscar elemento? → BINARY SEARCH",
        "funcion": "binary_search(v, number, low, high)  /  binary_search(v, number)",
        "estructura": "Recursivo: caso base low>high. Iterativo: while low<=high"
    },
    "Max Vector — Máximo DyV": {
        "color": "#aa00ff",
        "keywords": ["máximo", "divide y vencerás", "mitades", "comparar", "valor máximo"],
        "cuando": "Encontrar el máximo de un vector usando Divide y Vencerás.",
        "truco": "¿Máximo con DyV? → MAX VECTOR. 3 versiones: tradicional, dyv con slicing, dyv con índices.",
        "funcion": "max_vector_dyv_efficient(v, l, h)",
        "estructura": "Caso base l==h → v[l]. Divide en mitad, max de ambas mitades"
    },
    "Knapsack BT — Mochila Backtracking": {
        "color": "#ff2222",
        "keywords": ["mochila", "sin fracciones", "maximizar valor", "backtracking", "explorar combinaciones"],
        "cuando": "Mochila donde NO puedes fraccionar objetos. Explora todas las combinaciones.",
        "truco": "¿Mochila sin fracciones? → BT. Es_solución cuando no cabe ningún objeto más.",
        "funcion": "knapsack_bt(data, sol, best_sol, k)",
        "estructura": "data={n,W,w,v}, sol={o,v,w}, is_solution cuando w+min(w)>W"
    },
    "Mochila 0/1 BT": {
        "color": "#ff2222",
        "keywords": ["mochila 0/1", "enteros", "maximizar", "backtracking", "sin fracciones"],
        "cuando": "Igual que knapsack_bt pero cada objeto se lleva 0 o 1 veces (no múltiples).",
        "truco": "Diferencia con knapsack_bt: usa 'obj' en vez de 'o', y i+1 en la recursión.",
        "funcion": "knapsack_0_1(data, sol, best_sol, k)",
        "estructura": "data={n,W,w,v}, sol={obj,v,w}, i+1 en llamada recursiva"
    },
    "N-Queens — N Reinas": {
        "color": "#ff2222",
        "keywords": ["reinas", "tablero", "no se atacan", "columna", "diagonal", "backtracking"],
        "cuando": "Colocar N reinas en tablero NxN sin que se ataquen.",
        "truco": "¿Reinas en tablero? → NQUEENS. is_feasible verifica columna y dos diagonales.",
        "funcion": "nqueens(sol, n, found, row)",
        "estructura": "sol[row]=col, verificar columna ±i y diagonal ±i"
    },
    "Coloreo de Grafos": {
        "color": "#ff2222",
        "keywords": ["colorear", "colores", "adyacentes distintos", "m colores", "asignar franjas"],
        "cuando": "Asignar colores a nodos de un grafo de forma que adyacentes tengan colores distintos.",
        "truco": "¿Asignar recursos/franjas sin conflictos entre conectados? → COLOREO",
        "funcion": "coloring_va(g, m, sol, node)",
        "estructura": "is_feasible verifica que adyacentes con adj<node no tengan el mismo color"
    },
    "Laberinto BT": {
        "color": "#ff2222",
        "keywords": ["laberinto", "camino mínimo", "backtracking", "cuadrícula", "explorar caminos"],
        "cuando": "Encontrar el camino más corto en un laberinto explorando todas las rutas.",
        "truco": "¿Laberinto con BT? Marca celdas con el paso k, guarda la mejor solución.",
        "funcion": "labyrinth(lab, best, r, c, k)",
        "estructura": "is_feasible verifica límites y celda==0, is_better compara lab[n][m]<best[n][m]"
    },
}