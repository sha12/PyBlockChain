
from backend.blockchain.block import Block


class BlockChain:
    def __init__(self):
        self.chain = [Block.genesis_block()]

    def add_block(self, data):
        block = Block.mine_block(self.chain[-1], data)
        self.chain.append(block)

    def __repr__(self):
        return f"Blockchain: {self.chain}"


if __name__ == "__main__":
    bc = BlockChain()
    bc.add_block("One")
    bc.add_block("Two")
    print(bc)
