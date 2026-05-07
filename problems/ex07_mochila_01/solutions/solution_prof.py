import copy

def init_data(n, W, v, w):
    return {'n': n, 'W': W, 'w': w, 'v': v}

def init_sol(data):
    return {'obj': [0]*data['n'], 'w': 0, 'v': 0}

def add(sol, data, i):
    sol['obj'][i]  = 1
    sol['w']      += data['w'][i]
    sol['v']      += data['v'][i]

def remove(sol, data, i):
    sol['obj'][i]  = 0
    sol['w']      -= data['w'][i]
    sol['v']      -= data['v'][i]

def best(sol_1, sol_2):
    if sol_1['v'] > sol_2['v']:
        return copy.deepcopy(sol_1)
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
    return best_sol