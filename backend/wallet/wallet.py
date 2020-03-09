import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
# ec -- elliptical cryptography
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    Individual Wallet of miners.
    Keeps track of balance, transactions
    """

    def __init__(self, blockchain=None):
        self.address = str(uuid.uuid4())[0:8]
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()
        self.serialize_public_key()
        self.blockchain = blockchain

    @property
    def balance(self):
        return Wallet.calculate_balance(self.blockchain, self.address)

    def serialize_public_key(self):
        """
        Return the serialize version of public key
        """
        self.public_key = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                       format=serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')

    def sign(self, data):
        """
        Generate a signature based on data, private key
        """
        return decode_dss_signature(self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256())))

    @staticmethod
    def verify_signature(public_key, data, signature):
        """
        Verify a signature based on original public key and data
        """
        # public key should be deserialized as we are converting it a string for jsonifying in serialize public key method
        public_key_deserialized = serialization.load_pem_public_key(
            public_key.encode('utf=8'),
            default_backend())

        try:
            public_key_deserialized.verify(encode_dss_signature(*signature),
                                           json.dumps(data).encode('utf-8'),
                                           ec.ECDSA(hashes.SHA256())
                                           )
            return True
        except InvalidSignature:
            print("Signature is invalid")
            return False

    @staticmethod
    def calculate_balance(blockchain, address):
        """
        Calculate the balance of given address considering all transactions within the blockchain.

        Balance is sum of all output values that belong to the address since the most recent transaction by that address
        """
        balance = STARTING_BALANCE

        if not blockchain:
            return balance

        for block in blockchain.chain:
            for transaction in block.data:
                if transaction['input']['address'] == address:
                    # anytime the address conducts a transaction, it resets the balance
                    balance = transaction['output'][address]
                elif address in transaction['output']:
                    balance += transaction['output'][address]

        return balance


if __name__ == "__main__":
    wallet = Wallet()
    data = {"block": "chain"}
    signature = wallet.sign(data)
    print(signature)
    print(wallet.__dict__)
    valid = wallet.verify_signature(wallet.public_key, data, signature)
    print("Validation", valid)
