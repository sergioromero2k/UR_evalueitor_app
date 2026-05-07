# Alternativa: sin funcion best(), comparando directamente
import copy

def is_solution(sol, data):
    return sol['w'] + min(data['w']) > data['W']

def is_feasible(sol, data, i):
    return sol['w'] + data['w'][i] <= data['W']

def add(sol, data, i):
    sol['obj'][i] = 1
    sol['w']     += data['w'][i]
    sol['v']     += data['v'][i]

def remove(sol, data, i):
    sol['obj'][i] = 0
    sol['w']     -= data['w'][i]
    sol['v']     -= data['v'][i]

def knapsack_0_1(data, sol, best_sol, k):
    if is_solution(sol, data):
        if sol['v'] > best_sol['v']:
            best_sol = copy.deepcopy(sol)
    else:
        for i in range(k, data['n']):
            if is_feasible(sol, data, i):
                add(sol, data, i)
                best_sol = knapsack_0_1(data, sol, best_sol, i+1)
                remove(sol, data, i)
    return best_sol