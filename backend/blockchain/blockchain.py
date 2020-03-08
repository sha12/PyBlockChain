
from backend.blockchain.block import Block


class BlockChain:
    def __init__(self):
        self.chain = [Block.genesis_block()]

    def add_block(self, data):
        block = Block.mine_block(self.chain[-1], data)
        self.chain.append(block)

    def __repr__(self):
        return f"Blockchain: {self.chain}"

    @staticmethod
    def is_chain_valid(chain):
        """
        Validate the chain
        """

        if chain[0] != Block.genesis_block():
            raise Exception("The genesis block is not valid")

        for i in range(1, len(chain)):
            block = chain[i]
            last_block = chain[i-1]
            Block.is_block_valid(last_block, block)

    def replace_chain(self, chain):
        """
        Replace the local chain with the incoming chain, if below rules apply
            - The incoming is longer than the local one
            - Incoming chain is formatted properly
        """
        if(len(chain) <= len(self.chain)):
            raise Exception(
                'Incoming chain must be longer than the local chain')

        try:
            BlockChain.is_chain_valid(chain)
        except Exception as e:
            raise Exception(
                f"Cannot replace. The incoming chain is invalid: {e}")
        self.chain = chain


if __name__ == "__main__":
    bc = BlockChain()
    bc.add_block("One")
    bc.add_block("Two")
    print(bc)
