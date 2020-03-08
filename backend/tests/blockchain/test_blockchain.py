from backend.blockchain.blockchain import BlockChain
from backend.blockchain.block import GENESIS_DATA
import pytest


def test_blockchain():
    blockchain = BlockChain()

    assert blockchain.chain[0].hash == GENESIS_DATA['hash']


def test_add_block():
    blockchain = BlockChain()
    data = "test_data"
    blockchain.add_block(data)

    assert blockchain.chain[1].data == data


@pytest.fixture
def blockchain_ten_blocks():
    blockchain = BlockChain()
    for i in range(10):
        blockchain.add_block(i)
    return blockchain


def test_is_chain_valid(blockchain_ten_blocks):
    BlockChain.is_chain_valid(blockchain_ten_blocks.chain)


def test_is_chain_valid_bad_genesis(blockchain_ten_blocks):
    blockchain_ten_blocks.chain[0].hash = "bad_genesis_block"
    with pytest.raises(Exception, match="The genesis block is not valid"):
        BlockChain.is_chain_valid(blockchain_ten_blocks.chain)


def test_replace_chain(blockchain_ten_blocks):
    blockchain = BlockChain()
    blockchain.replace_chain(blockchain_ten_blocks.chain)

    assert blockchain.chain == blockchain_ten_blocks.chain


def test_replace_chain_not_longer(blockchain_ten_blocks):
    blockchain = BlockChain()
    with pytest.raises(Exception, match="Incoming chain must be longer than the local chain"):
        blockchain_ten_blocks.replace_chain(blockchain.chain)


def test_replace_chain_invalid_incoming_chain(blockchain_ten_blocks):
    blockchain = BlockChain()
    blockchain_ten_blocks.chain[1].hash = "tampered hash"
    with pytest.raises(Exception, match="Cannot replace. The incoming chain is invalid"):
        blockchain.replace_chain(blockchain_ten_blocks.chain)
