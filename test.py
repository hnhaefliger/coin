import coin

transactions = [
    coin.Transaction('a', 'b', 12) for i in range(12)
]

block = coin.Block(0, '', transactions, difficulty=6)

print(block.mine())