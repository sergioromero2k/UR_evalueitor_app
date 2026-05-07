import copy

def is_solution(sol, data):
    return sol['w'] + min(data['w']) > data['W']

def is_feasible(sol, data, i):
    return sol['w'] + data['w'][i] <= data['W']

def add(sol, data, i):
    sol['o'][i] += 1
    sol['v']    += data['v'][i]
    sol['w']    += data['w'][i]

def remove(sol, data, i):
    sol['o'][i] -= 1
    sol['v']    -= data['v'][i]
    sol['w']    -= data['w'][i]

def knapsack_bt(data, sol, best_sol, k):
    if is_solution(sol, data):
        if sol['v'] > best_sol['v']:
            best_sol = copy.deepcopy(sol)
    else:
        for i in range(k, data['n']):
            if is_feasible(sol, data, i):
                add(sol, data, i)
                best_sol = knapsack_bt(data, sol, best_sol, i)
                remove(sol, data, i)
    return best_sol