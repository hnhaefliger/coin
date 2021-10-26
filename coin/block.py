import hashlib
import json

class Block:
    def __init__(self, prev):
        self.prev = prev
        self.nonce = ''
        self.transactions = []

    def to_json(self):
        return {
            'prev': self.prev,
            'nonce': self.nonce,
            'transactions': [transaction.to_json() for transaction in self.transactions],
        }