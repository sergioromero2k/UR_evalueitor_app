# Alternativa: ordenar por beneficio directamente con sort
def greedy_schedule(names, profit, deadline):
    n = len(profit)
    items = sorted(range(n), key=lambda x: -profit[x])
    last_date = max(deadline)
    sol = [-1] * (last_date + 1)
    for i in items:
        d = deadline[i]
        while d > 0:
            if sol[d] == -1:
                sol[d] = i
                break
            d -= 1
    total = sum(profit[s] for s in sol if s != -1)
    print(total)
    for i in range(1, last_date + 1):
        if sol[i] != -1:
            print(f"DIA {i}: {names[sol[i]]}")