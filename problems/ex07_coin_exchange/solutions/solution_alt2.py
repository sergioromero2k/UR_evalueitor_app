# Alternativa: convirtiendo a enteros para evitar problemas de flotantes
def money_exchange(value, coins):
    FACTOR = 100
    value_int = round(value * FACTOR)
    coins_int = [round(c * FACTOR) for c in coins]
    result = []
    for coin in coins_int:
        result.append(value_int // coin)
        value_int = value_int % coin
    return result