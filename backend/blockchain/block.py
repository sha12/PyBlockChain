import time
from backend.utils.crypto_hash import crypto_hash


class Block:
    def __init__(self, timestamp, hash, last_hash, data):
        self.timestamp = timestamp
        self.hash = hash
        self.last_hash = last_hash
        self.data = data

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'hash: {self.hash}, '
            f'last_hash: {self.last_hash}, '
            f'data: {self.data})'
        )

    @staticmethod
    def mine_block(last_block, data):
        timestamp = time.time_ns()
        last_hash = last_block.hash
        hash = crypto_hash(timestamp, last_hash, data)
        return Block(timestamp, hash, last_hash, data)

    @staticmethod
    def genesis_block():
        return Block(1, '###', "####", "Genesis Block")


if __name__ == "__main__":
    genesis = Block.genesis_block()
    print(Block.mine_block(genesis, "First Block"))
