from backend.wallet.transaction_pool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import BlockChain


def test_add_transaction():
    transaction_pool = TransactionPool()
    transaction = Transaction(Wallet(), "abcd", 10)
    transaction_pool.add_transaction(transaction)

    assert transaction_pool.all_transactions[transaction.id] == transaction


def test_clear_transactions_added_to_blockchain():
    transaction_pool = TransactionPool()
    transaction_1 = Transaction(Wallet(), "abcd", 10)
    transaction_2 = Transaction(Wallet(), "abcd", 30)

    transaction_pool.add_transaction(transaction_1)
    transaction_pool.add_transaction(transaction_2)

    blockchain = BlockChain()
    blockchain.add_block([transaction_1.to_json(), transaction_2.to_json()])

    assert transaction_1.id in transaction_pool.all_transactions
    assert transaction_2.id in transaction_pool.all_transactions

    transaction_pool.clear_transactions_added_to_blockchain(blockchain)

    assert not transaction_1.id in transaction_pool.all_transactions
    assert not transaction_2.id in transaction_pool.all_transactions
