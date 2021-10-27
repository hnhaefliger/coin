import time
import hashlib

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.time = int(time.time())

        self.hash = self.compute_hash()

    def __str__(self):
        return self.sender + self.receiver + str(self.amount) + str(self.time)

    def compute_hash(self):
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

    def is_valid(self):
        if self.compute_hash() == self.hash:
            return True

    def as_json(self):
        return {
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'time': self.time,
            'hash': self.hash,
        }

test = Transaction('a', 'b', 12)
print(test.hash)
