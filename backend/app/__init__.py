import os
import random
import requests
from flask import Flask, jsonify, request
from backend.blockchain.blockchain import BlockChain
from backend.publish_subscribe import PubSub
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transaction_pool import TransactionPool
from flask_cors import CORS
from waitress import serve
import logging
from paste.translogger import TransLogger

logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

app = Flask(__name__)

CORS(app, resoources={r'/*': {'origins': 'http://localhost:3000'}})

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


@app.route('/blockchain/range')
def route_blockchain_range():
    start = int(request.args.get('start'))
    end = int(request.args.get('end'))
    return jsonify(blockchain.to_json()[::-1][start:end])


@app.route('/blockchain/length')
def route_blockchain_length():
    return jsonify(len(blockchain.chain))


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


@app.route("/frequent-addresses")
def route_known_addresses():
    known_address = set()
    for block in blockchain.chain:
        for transaction in block.data:
            known_address.update(transaction['output'].keys())
    return jsonify(list(known_address))


@app.route('/all-transactions')
def route_all_transactions():
    return jsonify(transaction_pool.transaction_data())


PORT = 5000

if os.environ.get('SEED_DATA') == 'True':
    for i in range(10):
        blockchain.add_block([Transaction(Wallet(), Wallet().address, random.randint(2, 20)).to_json(),
                              Transaction(Wallet(), Wallet().address, random.randint(2, 20)).to_json()])

    for i in range(5):
        transaction_pool.add_transaction(Transaction(
            Wallet(), Wallet().address, random.randint(2, 50)))

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

#serve(TransLogger(app, setup_console_handler=True))
