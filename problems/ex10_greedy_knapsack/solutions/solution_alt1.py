# Alternativa: ordenando directamente por ratio valor/peso
def greedy_knapsack(v, w, W):
    items  = sorted(range(len(v)), key=lambda i: v[i]/w[i], reverse=True)
    valor  = 0
    weight = 0
    for i in items:
        if weight + w[i] <= W:
            valor  += v[i]
            weight += w[i]
        else:
            fraccion = (W - weight) / w[i]
            valor   += v[i] * fraccion
            break
    print("{:.2f}".format(valor))