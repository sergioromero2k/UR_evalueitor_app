def max_vector_trad(v):
    m = v[0]
    for i in range(1, len(v)):
        m = max(m, v[i])
    return m

def max_vector_dyv(v):
    if len(v) == 1:
        return max_vector_trad(v)
    mitad = len(v) // 2
    izq   = max_vector_dyv(v[0:mitad])
    der   = max_vector_dyv(v[mitad:len(v)])
    return max(izq, der)

def max_vector_dyv_efficient(v, l, h):
    if l == h:
        return v[l]
    mitad = (l + h) // 2
    izq   = max_vector_dyv_efficient(v, l, mitad)
    der   = max_vector_dyv_efficient(v, mitad+1, h)
    return max(izq, der)