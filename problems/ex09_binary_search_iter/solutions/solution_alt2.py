# Alternativa: con flag de encontrado
def binary_search(v, number):
    low   = 0
    high  = len(v) - 1
    found = False
    pos   = -1
    while low <= high and not found:
        mid = (low + high) // 2
        if v[mid] == number:
            found = True
            pos   = mid
        elif number < v[mid]:
            high = mid - 1
        else:
            low = mid + 1
    if found:
        return pos
    return -low