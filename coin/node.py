from .blockchain import Blockchain
from .block import Block
from .transaction import Transaction
from .network import NetworkInterface

class Node:
    def __init__(self, other_nodes):
        self.network_interface = NetworkInterface(other_nodes, self.update_blockchain, self.update_blocks, self.update_transactions)
        
        self.transactions = []

        self.blockchain = Blockchain()

    def mine(self):
        # Choose transactions

        block = Block(len(self.blockchain), self.blockchain[-1].hash, self.transactions, difficulty=4)

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

    def update_transactions(self, sender, receiver, amount):
        balance = self.blockchain.get_balance(sender)

        for transaction in self.transactions:
            balance += transaction.get_balance(sender)

        if balance >= amount:
            self.transactions.append(Transaction(sender, receiver, amount))

            # Broadcast transaction

            return True

        return False

    

    
