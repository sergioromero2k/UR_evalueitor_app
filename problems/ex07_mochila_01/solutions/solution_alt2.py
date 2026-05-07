# Alternativa: con lista en vez de dict
import copy

def knapsack_0_1(data, sol, best_sol, k):
    if sol['w'] + min(data['w']) > data['W']:
        if sol['v'] > best_sol['v']:
            best_sol = copy.deepcopy(sol)
        return best_sol
    for i in range(k, data['n']):
        if sol['w'] + data['w'][i] <= data['W']:
            sol['obj'][i] = 1
            sol['v']     += data['v'][i]
            sol['w']     += data['w'][i]
            best_sol = knapsack_0_1(data, sol, best_sol, i+1)
            sol['obj'][i] = 0
            sol['v']     -= data['v'][i]
            sol['w']     -= data['w'][i]
    return best_sol