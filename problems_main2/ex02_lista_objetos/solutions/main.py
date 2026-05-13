from algoritmo import knapsack_0_1

def main():
    N, W = map(int, input().split())
    nombres, valores, pesos = [], [], []
    for _ in range(N):
        parts = input().split()
        nombres.append(parts[0])
        valores.append(int(parts[1]))
        pesos.append(int(parts[2]))

    data     = {'n': N, 'W': W, 'w': pesos, 'v': valores}
    sol      = {'obj': [0]*N, 'w': 0, 'v': 0}
    best_sol = {'obj': [0]*N, 'w': 0, 'v': 0}

    best_sol = knapsack_0_1(data, sol, best_sol, 0)

    print(best_sol['v'])
    seleccionados = sorted([nombres[i] for i in range(N) if best_sol['obj'][i] == 1])
    for nombre in seleccionados:
        print(nombre)

if __name__ == "__main__":
    main()