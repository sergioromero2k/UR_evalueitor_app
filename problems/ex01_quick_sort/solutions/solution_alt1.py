# Alternativa: particion de Lomuto
def partition(v, low, high):
    pivot = v[high]
    i = low - 1
    for j in range(low, high):
        if v[j] <= pivot:
            i += 1
            v[i], v[j] = v[j], v[i]
    v[i+1], v[high] = v[high], v[i+1]
    return i + 1

def quick_sort(v, i, j):
    if i >= j:
        return
    p = partition(v, i, j)
    quick_sort(v, i, p - 1)
    quick_sort(v, p + 1, j)