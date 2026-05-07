# Alternativa: iterativa
def binary_search(v, number, low, high):
    while low <= high:
        mid = (low + high) // 2
        if number == v[mid]:
            return mid
        if number < v[mid]:
            high = mid - 1
        else:
            low = mid + 1
    return low