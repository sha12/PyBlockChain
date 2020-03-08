import uuid
import time
from backend.wallet.wallet import Wallet


class Transaction:
    """
    Make transactions between wallets
    """

    def __init__(self, sender_wallet, recipient, amount):
        self.id = str(uuid.uuid4())[0:8]
        self.output = self.create_output(sender_wallet, recipient, amount)
        self.input = self.create_input(sender_wallet, self.output)

    def create_output(self, sender_wallet, recipient, amount):
        """
        Structure the output data of the transaction.
        """
        if amount > sender_wallet.balance:
            raise Exception("In sufficient balance")

        output = {}
        output[recipient] = amount
        output[sender_wallet.address] = sender_wallet.balance - amount
        return output

    def create_input(self, sender_wallet, output):
        """
        Structure the input data of the transaction.
        Sign the transaction and include sender's public key, address
        """
        return {
            'timestamp': time.time_ns(),
            'amount': sender_wallet.balance,
            'address': sender_wallet.address,
            'public_key': sender_wallet.public_key,
            'signature': sender_wallet.sign(output)
        }

    def update_transaction(self, sender_wallet, recipient, amount):
        """
        Update the transaction with new recipient.
        """
        if recipient in self.output:
            self.output[sender_wallet.address] += self.output[recipient]

        if amount > self.output[sender_wallet.address]:
            raise Exception("In sufficient balance")

        self.output[recipient] = amount
        self.output[sender_wallet.address] -= amount

        self.input = self.create_input(sender_wallet, self.output)

    @staticmethod
    def is_transaction_valid(transaction):
        """
        Verify if a transaction is valid.
        """
        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception(
                "Invalid transaction.  Input amount and sum of output amounts doesnt match")

        if not Wallet.verify_signature(transaction.input['public_key'], transaction.output, transaction.input['signature']):
            raise Exception("Invalid Signature")


if __name__ == "__main__":
    transaction = Transaction(Wallet(), 'recipient', 10)
    print(transaction.__dict__)
