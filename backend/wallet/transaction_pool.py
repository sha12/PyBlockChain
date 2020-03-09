class TransactionPool:
    def __init__(self):
        self.all_transactions = {}

    def add_transaction(self, transaction):
        """
        Add a transaction to the transaction pool
        """
        self.all_transactions[transaction.id] = transaction

    def find_transaction(self, address):
        """
        If a transaction from a address is already present in the pool,
        we have to add new recipient or update the existing recipient instead of creating a new transaction
        """
        for transaction in self.all_transactions.values():
            if transaction.input['address'] == address:
                return transaction

    def transaction_data(self):
        """
        Serializable transactions
        """
        return [transaction.to_json()
                for transaction in self.all_transactions.values()]

    def clear_transactions_added_to_blockchain(self, blockchain):
        """
        Remove the transactions which are added to blockchain from transaction pool.
        """
        for block in blockchain.chain:
            for transaction in block.data:
                try:
                    del self.all_transactions[transaction['id']]
                except KeyError:
                    pass
