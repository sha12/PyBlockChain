import requests
from backend.wallet.wallet import Wallet
import time

BASE_URL = "http://localhost:5000"


def get_blockchain():
    return requests.get(f"{BASE_URL}/blockchain").json()


def blockchain_mine():
    return requests.get(f'{BASE_URL}/blockchain/mine').json()


def do_wallet_transaction(recipient, amount):
    return requests.post(f'{BASE_URL}/wallet/transaction', json={
        'recipient': recipient,
        'amount': amount
    }).json()


def get_wallet_details():
    return requests.get(f'{BASE_URL}/wallet/details').json()


blockchain = get_blockchain()
print(f"blockchain: {blockchain}")

recipient = Wallet().address

transaction1 = do_wallet_transaction(recipient, 50)
print(f"\nTransaction 1: {transaction1}")


transaction2 = do_wallet_transaction(recipient, 100)
print(f"\nTransaction 2: {transaction2}")

time.sleep(1)
updated_blockchain = blockchain_mine()
print(f"\nMined Block: {updated_blockchain}")


print(f"\nWallet Details: {get_wallet_details()}")
