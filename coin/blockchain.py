from .block import Block
from .transaction import Transaction

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, '', [], difficulty=6)]
        self.chain[-1].mine()

        self.pending_transactions = []

    def get_balance(self, key):
        balance = 0

        for block in self.chain:
            balance += block.get_balance(key)

        return balance

    def is_valid(self):
        if all([block.index == i for i, block in enumerate(self.blocks)]):
            if all([block.is_valid() for block in self.blocks]):
                if all([self.blocks[i].prev == self.blocks[i-1].hash for i in range(1, len(self.blocks))]):
                    return True

        return False
    
    def add(self, sender, receiver, amount):
        if self.get_balance(sender) >= amount:
            self.pending_transactions.append(Transaction(sender, receiver, amount))

        return True

    def mine_new(self):
        self.chain.append(Block(self.chain[-1].index + 1, self.chain[-1].hash, self.pending_transactions, difficulty=4))
        self.chain[-1].mine()
        self.pending_transactions = []

        return True

    def __getitem__(self, idx):
        return self.chain[idx]

    def __len__(self):
        return len(self.chain)

    def as_json(self):
        return {
            'pending_transactions': [
                transaction.as_json() for transaction in self.pending_transactions
            ],
            'chain':[
                block.as_json() for block in self.chain
            ],
        }

    @staticmethod
    def from_json(self, json):
        blockchain = Blockchain()

        blockchain.pending_transactions = [Transaction.from_json(transaction) for transaction in json['pending_transactions']]
        blockchain.chain = [Block.from_json(block) for block in json['chain']]

        if blockchain.is_valid():
            return blockchain

        return False