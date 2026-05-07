# Alternativa: recursiva con indice negativo si no encuentra
def binary_search(v, number, low, high):
    if low > high:
        return low
    mid = (low + high) // 2
    if v[mid] == number:
        return mid
    elif number < v[mid]:
        return binary_search(v, number, low, mid-1)
    else:
        return binary_search(v, number, mid+1, high)