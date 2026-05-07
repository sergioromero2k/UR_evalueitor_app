# Alternativa: merge_sort devuelve lista nueva en vez de modificar in-place
def merge_sort(v):
    if len(v) <= 1:
        return
    mid   = len(v) // 2
    left  = v[:mid]
    right = v[mid:]
    merge_sort(left)
    merge_sort(right)
    i = j = k = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            v[k] = left[i]; i += 1
        else:
            v[k] = right[j]; j += 1
        k += 1
    while i < len(left):
        v[k] = left[i]; i += 1; k += 1
    while j < len(right):
        v[k] = right[j]; j += 1; k += 1