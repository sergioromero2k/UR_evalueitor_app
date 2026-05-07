# Alternativa: pivot aleatorio
import random

def quick_sort(v, i, j):
    if i >= j:
        return
    pivot_idx = random.randint(i, j)
    v[i], v[pivot_idx] = v[pivot_idx], v[i]
    pivot = v[i]
    left  = i + 1
    right = j
    while left <= right:
        if v[left] <= pivot:
            left += 1
        else:
            v[left], v[right] = v[right], v[left]
            right -= 1
    v[i], v[right] = v[right], v[i]
    quick_sort(v, i, right - 1)
    quick_sort(v, right + 1, j)