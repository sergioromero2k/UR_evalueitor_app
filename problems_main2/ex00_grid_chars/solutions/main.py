import copy
from algoritmo import labyrinth

def main():
    N, M = map(int, input().split())
    grid = []
    for _ in range(N):
        grid.append(input().split())

    start = end = None
    for i in range(N):
        for j in range(M):
            if grid[i][j] == 'S': start = (i, j)
            elif grid[i][j] == 'T': end   = (i, j)

    lab = []
    for i in range(N):
        row = []
        for j in range(M):
            if grid[i][j] in ('W', 'F'):
                row.append(-1)
            else:
                row.append(0)
        lab.append(row)

    k = 1
    lab[start[0]][start[1]] = k
    best = copy.deepcopy(lab)
    best[end[0]][end[1]] = 0x3f3f3f3f

    best = labyrinth(lab, best, start[0], start[1], k+1)

    if best[end[0]][end[1]] == 0x3f3f3f3f:
        print("IMPOSIBLE")
    else:
        print(best[end[0]][end[1]] - 1)

if __name__ == "__main__":
    main()