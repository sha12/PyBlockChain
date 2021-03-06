from backend.blockchain.blockchain import BlockChain
from backend.blockchain.block import GENESIS_DATA
import pytest
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet


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
    for i in range(5):
        blockchain.add_block([Transaction(Wallet(), 'abcd', i).to_json()])
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


def test_is_transaction_chain_valid(blockchain_ten_blocks):
    BlockChain.is_transaction_chain_valid(blockchain_ten_blocks.chain)


def test_is_transaction_chain_valid_duplicate_transactions(blockchain_ten_blocks):
    blockchain_ten_blocks.chain.append(blockchain_ten_blocks.chain[3])
    with pytest.raises(Exception, match="is not unique"):
        BlockChain.is_transaction_chain_valid(blockchain_ten_blocks.chain)


def test_is_transaction_chain_valid_multiple_rewards(blockchain_ten_blocks):
    reward1 = Transaction.reward(Wallet()).to_json()
    reward2 = Transaction.reward(Wallet()).to_json()
    blockchain_ten_blocks.add_block([reward1, reward2])

    with pytest.raises(Exception, match="Duplicate mining reward in block"):
        BlockChain.is_transaction_chain_valid(blockchain_ten_blocks.chain)


def test_is_transaction_chain_valid_corrupt_transaction(blockchain_ten_blocks):
    corrupt_transaction = Transaction(Wallet(), 'recipient', 1)

    corrupt_transaction.input['signature'] = Wallet().sign({"a": "b"})
    blockchain_ten_blocks.add_block([corrupt_transaction.to_json()])
    with pytest.raises(Exception):
        BlockChain.is_transaction_chain_valid(blockchain_ten_blocks.chain)


def test_is_transaction_chain_valid_balance_tillnow(blockchain_ten_blocks):
    wallet = Wallet()
    corrupt_transaction = Transaction(wallet, "abcd", 10)
    corrupt_transaction.output[wallet.address] = 9000
    corrupt_transaction.input['amount'] = 9010
    corrupt_transaction.input['signature'] = wallet.sign(
        corrupt_transaction.output)

    blockchain_ten_blocks.add_block([corrupt_transaction.to_json()])

    with pytest.raises(Exception):
        BlockChain.is_transaction_chain_valid(blockchain_ten_blocks.chain)
