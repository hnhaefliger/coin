from .blockchain import Blockchain
from .block import Block
from .transaction import Transaction
from .nodeconnection import NodeConnection

class Node:
    def __init__(self, other_nodes):
        self.node_connections = [NodeConnection(node) for node in other_nodes]
        
        self.pending_transactions = []

        self.blockchain = Blockchain()

    def mine(self):
        # Choose transactions

        block = Block(len(self.blockchain), self.blockchain[-1].hash, self.pending_transactions, difficulty=4)

        if block.mine():
            self.update_blocks(block)

            # Broadcast new block

        return True

    def update_blocks(self, new_block):
        # remove transactions
        # account for branches

        return self.blockchain.add(new_block)

    def update_blockchain(self, new_blockchain):
        if new_blockchain.is_valid:
            if len(new_blockchain) > len(self.blockchain):
                self.blockchain = new_blockchain

                return True

        return False

    def transaction(self, sender, receiver, amount):
        balance = self.blockchain.get_balance(sender)

        for transaction in self.pending_transactions:
            balance += transaction.get_balance(sender)

        if balance >= amount:
            self.pending_transactions.append(Transaction(sender, receiver, amount))

            # Broadcast transaction

            return True

        return False

    

    
