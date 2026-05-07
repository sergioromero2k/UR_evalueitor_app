def money_exchange(value, coins):
    exchange = [0] * len(coins)
    i = 0
    while i < len(coins) and value >= 0:
        exchange[i] = int(value // coins[i])
        value = round(value % coins[i], 10)
        i += 1
    return exchange