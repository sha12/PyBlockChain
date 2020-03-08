from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet
import pytest


def test_transaction():
    sender_wallet = Wallet()
    recipient = "giveto"
    amount = 50
    transaction = Transaction(sender_wallet, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender_wallet.address] == sender_wallet.balance - amount

    assert 'timestamp' in transaction.input
    assert transaction.input['amount'] == sender_wallet.balance

    assert transaction.input['public_key'] == sender_wallet.public_key

    assert Wallet.verify_signature(
        transaction.input['public_key'], transaction.output, transaction.input['signature'])


def test_transaction_in_sufficient_balance():
    with pytest.raises(Exception, match="In sufficient balance"):
        Transaction(Wallet(), 'recipient', 1001)


def test_transaction_update_in_sufficient_balance():
    sender_wallet = Wallet()
    recipient = "abcd"
    amount = 500
    transaction = Transaction(sender_wallet, recipient, amount)
    with pytest.raises(Exception, match="In sufficient balance"):
        transaction.update_transaction(sender_wallet, "abcde", 1000)


def test_transaction_update():
    sender_wallet = Wallet()
    recipient = "abcd"
    amount = 500
    transaction = Transaction(sender_wallet, recipient, amount)

    transaction.update_transaction(sender_wallet, "abcde", 300)
    transaction.update_transaction(sender_wallet, "abcd", 700)

    assert transaction.output[recipient] == 700
    assert transaction.output[sender_wallet.address] == 0

    assert Wallet.verify_signature(
        transaction.input['public_key'], transaction.output, transaction.input['signature'])


def test_valid_transaction():
    transaction = Transaction(Wallet(), "abcd", 20)
    Transaction.is_transaction_valid(transaction)


def test_is_transaction_valid_with_invalid_outputs():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'abcd', 50)

    transaction.output[sender_wallet.address] = 1001

    with pytest.raises(Exception, match="Invalid transaction.  Input amount and sum of output amounts doesnt match"):
        Transaction.is_transaction_valid(transaction)


def test_is_transaction_valid_with_invalid_signature():
    sender_wallet = Wallet()
    transaction = Transaction(sender_wallet, 'abcd', 50)

    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match="Invalid Signature"):
        Transaction.is_transaction_valid(transaction)
