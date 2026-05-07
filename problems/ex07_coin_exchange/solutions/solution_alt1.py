# Alternativa: usando math.floor para evitar errores de punto flotante
import math

def money_exchange(value, coins):
    result = []
    for coin in coins:
        count = math.floor(round(value / coin, 10))
        result.append(count)
        value = round(value - count * coin, 10)
    return result