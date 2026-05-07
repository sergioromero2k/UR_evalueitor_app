def get_best_item(candidates, v, w):
    best_item  = 0
    best_ratio = -1
    for c in candidates:
        ratio = v[c] / w[c]
        if ratio > best_ratio:
            best_item  = c
            best_ratio = ratio
    return best_item

def greedy_knapsack(v, w, W):
    candidates = set(range(len(v)))
    sol    = [0] * len(v)
    weight = 0
    valor  = 0
    while candidates and weight < W:
        best = get_best_item(candidates, v, w)
        candidates.remove(best)
        if w[best] + weight <= W:
            sol[best] = 1
            weight += w[best]
            valor  += v[best]
        else:
            fraccion   = (W - weight) / w[best]
            sol[best]  = fraccion
            valor     += v[best] * fraccion
            weight     = W
    print("{:.2f}".format(valor))