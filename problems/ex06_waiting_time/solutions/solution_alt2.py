# Alternativa: índices ordenados por tiempo con cálculo acumulado
def order_tasks(names, tasks):
    orden = sorted(range(len(tasks)), key=lambda x: tasks[x])
    print(*[names[i] for i in orden])
    espera = 0
    acum   = 0
    for i in orden:
        espera += acum
        acum   += tasks[i]
    print(espera)