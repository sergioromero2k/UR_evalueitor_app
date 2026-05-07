# Alternativa: usando lista de tareas ordenadas y slots disponibles
def greedy_schedule(names, profit, deadline):
    tareas = sorted(zip(profit, deadline, names), reverse=True)
    last_date = max(deadline)
    sol = {}
    for b, d, name in tareas:
        for slot in range(d, 0, -1):
            if slot not in sol:
                sol[slot] = (name, b)
                break
    total = sum(v for _, (_, v) in sol.items())
    print(total)
    for dia in sorted(sol):
        print(f"DIA {dia}: {sol[dia][0]}")