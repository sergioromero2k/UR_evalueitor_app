# Alternativa: iterativa pura
def max_vector_dyv_efficient(v, l, h):
    m = v[l]
    for i in range(l+1, h+1):
        if v[i] > m:
            m = v[i]
    return m