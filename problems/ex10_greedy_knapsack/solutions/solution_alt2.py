# Alternativa: con lista de tuplas (ratio, valor, peso)
def greedy_knapsack(v, w, W):
    items = sorted(
        [(v[i]/w[i], v[i], w[i]) for i in range(len(v))],
        reverse=True
    )
    valor     = 0.0
    capacidad = W
    for ratio, vi, wi in items:
        if capacidad <= 0:
            break
        if wi <= capacidad:
            valor     += vi
            capacidad -= wi
        else:
            valor     += vi * (capacidad / wi)
            capacidad  = 0
    print("{:.2f}".format(valor))