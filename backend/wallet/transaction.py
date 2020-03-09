import uuid
import time
from backend.wallet.wallet import Wallet
from backend.config import MINIING_REWARD, MINIING_REWARD_INPUT


class Transaction:
    """
    Make transactions between wallets
    """

    def __init__(self, sender_wallet=None, recipient=None, amount=None, id=None, output=None, input=None):
        self.id = id or str(uuid.uuid4())[0:8]
        self.output = output or self.create_output(
            sender_wallet, recipient, amount)
        self.input = input or self.create_input(sender_wallet, self.output)

    def to_json(self):
        return self.__dict__

    @staticmethod
    def from_json(transaction_json):
        """
        Deserialize transaction json and return a transaction Object
        """
        return Transaction(**transaction_json)

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

        if transaction.input == MINIING_REWARD_INPUT:
            if list(transaction.output.values())[0] != MINIING_REWARD:
                raise Exception("Invalid reward transaction")
            return

        output_total = sum(transaction.output.values())

        if transaction.input['amount'] != output_total:
            raise Exception(
                "Invalid transaction.  Input amount and sum of output amounts doesnt match")

        if not Wallet.verify_signature(transaction.input['public_key'], transaction.output, transaction.input['signature']):
            raise Exception("Invalid Signature")

    @staticmethod
    def reward(miner_wallet):
        """
        Returns a reward for the miner.
        """
        output = {miner_wallet.address: MINIING_REWARD}
        return Transaction(input=MINIING_REWARD_INPUT, output=output)


if __name__ == "__main__":
    transaction = Transaction(Wallet(), 'recipient', 10)
    print(transaction.__dict__)
    transaction1 = Transaction.from_json(transaction.to_json())
    print(transaction1.__dict__)
