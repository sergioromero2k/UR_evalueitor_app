import copy
from algoritmo import labyrinth

def main():
    N, M = map(int, input().split())
    grid = []
    for _ in range(N):
        grid.append(list(map(int, input().split())))

    # En este problema el grid ya es numerico
    # -1 = pared, >0 = transitable hasta ese turno
    # Construir lab: celdas transitables = 0, paredes = -1
    # pero necesitamos respetar el limite de turnos
    # La celda (0,0) es el inicio con k=1
    lab = []
    for i in range(N):
        row = []
        for j in range(M):
            if grid[i][j] == -1:
                row.append(-1)
            else:
                row.append(0)
        lab.append(row)

    k = 1
    lab[0][0] = k
    best = copy.deepcopy(lab)
    best[N-1][M-1] = 0x3f3f3f3f

    best = labyrinth(lab, best, 0, 0, k+1)

    if best[N-1][M-1] == 0x3f3f3f3f:
        print("NO HAY SALIDA")
    else:
        print(best[N-1][M-1] - 1)

if __name__ == "__main__":
    main()