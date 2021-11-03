import random
import socket
import threading
import struct
import json

class NetworkInterface:
    def __init__(self, nodes, update_blockchain, update_blocks, update_transactions, port=8040):
        self.server = socket.create_server((socket.gethostbyname(socket.gethostname()), port))
        self.server.listen()

        # communicate with announce (identify self, get peers)

        self.nodes = [self.server]

        for i in range(min([5, len(nodes)])):
            # better way of selecting nodes to connect to in order to protect network fully-connectedness
            node = random.choice(nodes)
            nodes.remove(node)
            self.nodes.append(socket.create_connection(node, 3))

        self.update_blockchain = update_blockchain
        self.update_blocks = update_blocks
        self.update_transactions = update_transactions

    def listen(self):
        while True:
            self.server.accept()

            for node in self.nodes:
                message_type, payload = self.recieve(node)

                if message_type == 1:
                    self.update_blockchain(payload)

                elif message_type == 2:
                    self.update_blocks(payload)

                elif message_type == 3:
                    self.update_transactions(payload)

            # check sufficient peers

            # check keepalive

    def receive(self, node):
        try:
            length = struct.unpack('>I', node.recv(4))

            if length > 0:
                (message_type, payload) = struct.unpack(f'>B{str(length - 1)}s', node.recv(length))

                return (length, message_type, payload)

            else:
                return (0, 0, '')

        except:
            self.disconnect()

    def send(self, message):
        for node in self.nodes:
            try:
                node.send(message)

            except:
                self.disconnect()

    def send_keepalive(self):
        message = struct.pack('>I', 0)

        return self.send(message)

    def send_blockchain(self, blockchain):
        blockchain = json.dumps(blockchain.as_json())
        message = struct.pack(f'>IB{len(blockchain)}s', len(blockchain) + 1, 1, blockchain)

        return self.send(message)

    def send_block(self, block):
        block = json.dumps(block.as_json())
        message = struct.pack(f'>IB{len(block)}s', len(block) + 1, 1, block)

        return self.send(message)

    def send_transaction(self, transaction):
        transaction = json.dumps(transaction.as_json())
        message = struct.pack(f'>IB{len(transaction)}s', len(transaction) + 1, 1, transaction)

        return self.send(message)

    def disconnect(self):
        pass
