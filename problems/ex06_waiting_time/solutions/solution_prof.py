def get_best_task(candidates, tasks):
    best_task = 0
    best_task_time = 0x3f3f3f3f
    for c in candidates:
        if tasks[c] < best_task_time:
            best_task = c
            best_task_time = tasks[c]
    return best_task

def order_tasks(names, tasks):
    candidates = set(range(len(tasks)))
    sol = []
    while candidates:
        best = get_best_task(candidates, tasks)
        candidates.remove(best)
        sol.append(best)
    print(*[names[i] for i in sol])
    accum = 0
    total = 0
    for i in sol:
        accum += tasks[i]
        total += accum - tasks[i]
    print(total)