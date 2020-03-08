import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block

pnconfig = PNConfiguration()

pnconfig.publish_key = "pub-c-55a4e7eb-225a-4f59-aa52-6db604fb8366"
pnconfig.subscribe_key = "sub-c-f228159c-6118-11ea-9c0b-5aef0d0da10f"

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain):
        self.blockchain = blockchain

    def message(self, pubnub, message_object):
        print(
            f"Message: {message_object.message} on Channel: {message_object.channel}")
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.from_json(message_object.message)
            updated_chain = self.blockchain.chain[:]
            updated_chain.append(block)
            try:
                self.blockchain.replace_chain(updated_chain)
                print("Successfully Updated the chain!")
            except Exception as e:
                print(f"Chain update failed: {e}")


class PubSub():
    """
    Handles publish, subscribe part of application.
    Provides communication between the nodes of blockchain network
    """

    def __init__(self, blockchain):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain))

    def publish(self, channel, message):
        """
        Publish the message object to given channel
        """
        self.pubnub.publish().channel(channel).message(message).sync()

    def broadcast_block(self, block):
        """
        Broadcast a block object to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.to_json())


if __name__ == "__main__":
    time.sleep(1)
    pubsub = PubSub()
    pubsub.publish(CHANNELS['TEST'], {'pub': 'nub'})
