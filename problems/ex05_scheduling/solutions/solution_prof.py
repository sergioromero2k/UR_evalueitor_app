def get_best_item(candidates, profit):
    best_item = -1
    best_profit = -1
    for c in candidates:
        if profit[c] > best_profit:
            best_profit = profit[c]
            best_item = c
    return best_item

def greedy_schedule(names, profit, deadline):
    n = len(profit)
    candidates = set(range(n))
    last_date = max(deadline)
    sol = [-1] * (last_date + 1)
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
    total = sum(profit[s] for s in sol if s != -1)
    print(total)
    for i in range(1, last_date + 1):
        if sol[i] != -1:
            print(f"DIA {i}: {names[sol[i]]}")