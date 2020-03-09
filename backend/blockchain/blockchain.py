
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction
from backend.config import MINIING_REWARD, MINIING_REWARD_INPUT
from backend.wallet.wallet import Wallet


class BlockChain:
    def __init__(self):
        self.chain = [Block.genesis_block()]

    def add_block(self, data):
        block = Block.mine_block(self.chain[-1], data)
        self.chain.append(block)

    def __repr__(self):
        return f"Blockchain: {self.chain}"

    def to_json(self):
        return [block.to_json() for block in self.chain]

    @staticmethod
    def from_json(chain_json):
        """
        reserialize list of serialized blocks to Blockchain object.
        """
        blockchain = BlockChain()
        blockchain.chain = [Block.from_json(
            block_json) for block_json in chain_json]
        return blockchain

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
        BlockChain.is_transaction_chain_valid(chain)

    @staticmethod
    def is_transaction_chain_valid(chain):
        """
        Validate chain with blocks of transactions
         -- Only one reward per transaction.
         -- Each transaction must only apprear once in chain.
        """
        transaction_ids = []
        for i in range(len(chain)):
            block = chain[i]
            contains_mining_reward = False
            for transaction_json in block.data:
                transaction_obj = Transaction.from_json(transaction_json)

                if transaction_obj.id in transaction_ids:
                    raise Exception(
                        f"Transaction: {transaction_obj.id} is not unique")

                transaction_ids.append(transaction_obj.id)

                if transaction_obj.input == MINIING_REWARD_INPUT:
                    if contains_mining_reward:
                        raise Exception(
                            f'Duplicate mining reward in block: {block.hash}')
                    contains_mining_reward = True
                else:
                    blockchain_tillnow = BlockChain()
                    blockchain_tillnow.chain = chain[0:i]
                    balance_tillnow = Wallet.calculate_balance(
                        blockchain_tillnow,
                        transaction_obj.input["address"]
                    )
                    if balance_tillnow != transaction_obj.input["amount"]:
                        raise Exception(
                            f"Transaction: {transaction_obj.id} has invalid input")

                Transaction.is_transaction_valid(transaction_obj)

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
