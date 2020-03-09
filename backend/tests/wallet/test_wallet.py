from backend.wallet.wallet import Wallet
from backend.blockchain.blockchain import BlockChain
from backend.config import STARTING_BALANCE
from backend.wallet.transaction import Transaction


def test_verify_signature():
    data = {"block": "chain"}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify_signature(wallet.public_key, data, signature)


def test_verify_invalid_signature():
    data = {"block": "chain"}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify_signature(Wallet().public_key, data, signature)


def test_calculate_balance():
    blockchain = BlockChain()
    wallet = Wallet()
    assert wallet.calculate_balance(
        blockchain, wallet.address) == STARTING_BALANCE

    sent_amount = 100
    transaction = Transaction(wallet, "abcd", sent_amount)
    blockchain.add_block([transaction.to_json()])
    assert wallet.calculate_balance(
        blockchain, wallet.address) == STARTING_BALANCE - sent_amount

    received_amount_1 = 100
    received_1 = Transaction(
        Wallet(),
        wallet.address,
        received_amount_1
    )

    received_amount_2 = 100
    received_2 = Transaction(
        Wallet(),
        wallet.address,
        received_amount_2
    )

    blockchain.add_block([received_1.to_json(), received_2.to_json()])
    assert wallet.calculate_balance(blockchain, wallet.address) == STARTING_BALANCE - \
        sent_amount + received_amount_1 + received_amount_2
