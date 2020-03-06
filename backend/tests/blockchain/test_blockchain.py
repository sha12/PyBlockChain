from backend.blockchain.blockchain import BlockChain
from backend.blockchain.block import GENESIS_DATA


def test_blockchain():
    blockchain = BlockChain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    blockchain = BlockChain()
    data = "test_data"
    blockchain.add_block(data)

    assert blockchain.chain[1].data == data
