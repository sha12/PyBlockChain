import time
from backend.utils.crypto_hash import crypto_hash
from backend.config import MINE_RATE
from backend.utils.hex_to_binary import hex_to_binary

GENESIS_DATA = {
    'timestamp': 1,
    'last_hash': 'NA',
    'hash': 'genesis_hash',
    'data': '',
    'difficulty': 3,
    'nonce': 'genesis_nonce'
}


class Block:
    def __init__(self, timestamp, hash, last_hash, data, difficulty, nonce):
        self.timestamp = timestamp
        self.hash = hash
        self.last_hash = last_hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block('
            f'timestamp: {self.timestamp}, '
            f'hash: {self.hash}, '
            f'last_hash: {self.last_hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce})'
        )

    @staticmethod
    def mine_block(last_block, data):
        """
        Mine a block with the details of last block and the data of the block to be created.
        Hash of the new block to be created should match the proof of work requirement of leading zeros.

        """
        timestamp = time.time_ns()
        last_hash = last_block.hash
        difficulty = Block.adjust_difficulty(last_block, timestamp)
        nonce = 0
        hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        while hex_to_binary(hash)[0:difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjust_difficulty(last_block, timestamp)
            hash = crypto_hash(timestamp, last_hash, data, difficulty, nonce)

        return Block(timestamp, hash, last_hash, data, difficulty, nonce)

    @staticmethod
    def genesis_block():
        return Block(**GENESIS_DATA)

    @staticmethod
    def adjust_difficulty(last_block, new_timestamp):
        """
        Calculate the time difference between the old block and new block to be added,
        and adjust difficulty
        """
        if(new_timestamp - last_block.timestamp) < MINE_RATE:
            return last_block.difficulty + 1
        return last_block.difficulty - 1 if last_block.difficulty-1 > 0 else 1


if __name__ == "__main__":
    genesis = Block.genesis_block()
    print(Block.mine_block(genesis, "First Block in the block chain"))
