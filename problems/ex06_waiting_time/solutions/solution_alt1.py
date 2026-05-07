# Alternativa: ordenar directamente por tiempo
def order_tasks(names, tasks):
    paired = sorted(zip(tasks, names), key=lambda x: x[0])
    print(*[name for _, name in paired])
    accum = 0
    total = 0
    for t, _ in paired:
        total += accum
        accum += t
    print(total)