import hashlib
import time

from .transaction import Transaction


class Block:
    def __init__(self, index, prev, transactions, difficulty=4):
        self.index = index
        self.prev = prev
        self.time = int(time.time())
        self.nonce = 0
        self.transactions = []

        self.difficulty = difficulty

        self.hash = self.compute_hash()

    def __str__(self):
        return str(self.nonce) + self.prev + str(self.index) + str(self.time) + ''.join([transaction.hash for transaction in self.transactions])

    def compute_hash(self):
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

    def mine(self):
        while self.compute_hash()[:self.difficulty] != '0' * self.difficulty:
            self.nonce += 1

        self.hash = self.compute_hash()

        return True

    def get_balance(self, key):
        balance = 0

        for transaction in self.transactions:
            balance += transaction.get_balance(key)

        return balance

    def is_valid(self):
        if all([transaction.is_valid() for transaction in self.transactions]):
            if self.compute_hash() == self.hash():
                if self.hash[:self.difficulty] == '0' * self.difficulty:
                    return True

        return False

    def __len__(self):
        return len(self.transactions)

    def __getitem__(self, idx):
        return self.transactions[idx]

    def as_json(self):
        return {
            'index': self.index,
            'prev': self.prev,
            'time': self.time,
            'nonce': self.nonce,
            'transactions': [
                transaction.as_json() for transaction in self.transactions
            ],
            'difficulty': self.difficulty,
            'hash': self.hash,
        }

    @staticmethod
    def from_json(json):
        block = Block(
            json['index'],
            json['prev'],
            [
                Transaction.from_json(transaction) for transaction in json['transactions']
            ],
            difficulty=json['difficulty']
        )


