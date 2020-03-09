import os
import random
import requests
from flask import Flask, jsonify, request
from backend.blockchain.blockchain import BlockChain
from backend.publish_subscribe import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool


app = Flask(__name__)
blockchain = BlockChain()
wallet = Wallet(blockchain)
transaction_pool = TransactionPool()
pubsub = PubSub(blockchain, transaction_pool)


@app.route('/')
def route_home():
    return "Home"


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_mine_block():
    """
    Adds a block to local block chain and broadcasts it to all nodes
    """
    transaction_data = transaction_pool.transaction_data()
    transaction_data.append(Transaction.reward(wallet).to_json())
    blockchain.add_block(transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    transaction_pool.clear_transactions_added_to_blockchain(blockchain)
    return jsonify(block.to_json())


@app.route('/wallet/transaction', methods=['POST'])
def route_make_transaction():
    transacation_data = request.get_json()
    transaction = transaction_pool.find_transaction(wallet.address)
    if transaction:
        transaction.update_transaction(
            wallet, transacation_data["recipient"], transacation_data["amount"])
    else:
        transaction = Transaction(
            wallet, transacation_data['recipient'], transacation_data['amount'])
    pubsub.broadcast_transaction(transaction)
    return jsonify(transaction.to_json())


@app.route('/wallet/details')
def route_wallet_details():
    return jsonify({'address': wallet.address, 'balance': wallet.balance})


PORT = 5000

if os.environ.get('PEER') == "True":
    result = requests.get('http://localhost:5000/blockchain')
    full_blockchain = BlockChain.from_json(result.json())
    PORT = random.randint(5001, 6000)
    try:
        blockchain.replace_chain(full_blockchain.chain)
        print("\n -- Successfully synchronized the local blockchain")
    except Exception as e:
        print(f"\n -- Failed to Synchroniz the local blockchain: {e}")

app.run(port=PORT)
