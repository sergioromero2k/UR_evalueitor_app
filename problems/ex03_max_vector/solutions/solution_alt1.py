# Alternativa: solo la version eficiente con indices
def max_vector_dyv_efficient(v, l, h):
    if l == h:
        return v[l]
    if h - l == 1:
        return max(v[l], v[h])
    mid = (l + h) // 2
    return max(
        max_vector_dyv_efficient(v, l, mid),
        max_vector_dyv_efficient(v, mid+1, h)
    )