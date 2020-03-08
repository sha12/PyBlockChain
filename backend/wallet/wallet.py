import uuid
import json
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
# ec -- elliptical cryptography
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature


class Wallet:
    """
    Individual Wallet of miners.
    Keeps track of balance, transactions
    """

    def __init__(self):
        self.address = str(uuid.uuid4())[0:8]
        self.balance = STARTING_BALANCE
        self.private_key = ec.generate_private_key(
            ec.SECP256K1(), default_backend())
        self.public_key = self.private_key.public_key()

    def sign(self, data):
        """
        Generate a signature based on data, private key
        """
        return self.private_key.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA256()))

    @staticmethod
    def verify_signature(public_key, data, signature):
        """
        Verify a signature based on original public key and data
        """
        try:
            public_key.verify(signature,
                              json.dumps(data).encode('utf-8'),
                              ec.ECDSA(hashes.SHA256())
                              )
            return True
        except InvalidSignature:
            print("Signature is invalid")
            return False


if __name__ == "__main__":
    wallet = Wallet()
    data = {"block": "chain"}
    signature = wallet.sign(data)
    valid = wallet.verify_signature(wallet.public_key, data, signature)
    print("Validation", valid)
