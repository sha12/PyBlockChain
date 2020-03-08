from backend.wallet.wallet import Wallet


def test_verify_signature():
    data = {"block": "chain"}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify_signature(wallet.public_key, data, signature)


def test_verify_invalid_signature():
    data = {"block": "chain"}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify_signature(Wallet().public_key, data, signature)
