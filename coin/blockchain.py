from .block import Block

class Blockchain:
    def __init__(self):
        self.chain = [Block(0, '', [], difficulty=6)]
        self.chain[-1].mine()

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
    
    def add(self, block):
        if block.prev == self.chain[-1].hash:
            if block.is_valid():
                block.index = len(self.chain)
                self.chain.append(block)
                return True

        return False

    def __getitem__(self, idx):
        return self.chain[idx]

    def __len__(self):
        return len(self.chain)

    def as_json(self):
        return {
            'chain':[
                block.as_json() for block in self.chain
            ],
        }

    @staticmethod
    def from_json(self, json):
        blockchain = Blockchain()

        blockchain.chain = [Block.from_json(block) for block in json['chain']]

        if blockchain.is_valid():
            return blockchain

        return False
