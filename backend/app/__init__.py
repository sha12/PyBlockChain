import os
import random
import requests
from flask import Flask, jsonify
from backend.blockchain.blockchain import BlockChain
from backend.publish_subscribe import PubSub

app = Flask(__name__)
blockchain = BlockChain()
pubsub = PubSub(blockchain)


@app.route('/')
def route_home():
    return "Home"


@app.route('/blockchain')
def route_blockchain():
    return jsonify(blockchain.to_json())


@app.route('/blockchain/mine')
def route_mine_block():
    transaction_data = "dummy_transaction_data"
    blockchain.add_block(data=transaction_data)
    block = blockchain.chain[-1]
    pubsub.broadcast_block(block)
    return jsonify(block.to_json())


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
