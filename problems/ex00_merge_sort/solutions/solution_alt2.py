# Alternativa: usando sorted() de Python internamente
def merge_sort(v):
    if len(v) <= 1:
        return
    mid   = len(v) // 2
    left  = v[:mid]
    right = v[mid:]
    merge_sort(left)
    merge_sort(right)
    result = []
    i = j  = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result += left[i:]
    result += right[j:]
    for k in range(len(v)):
        v[k] = result[k]