from backend.utils.crypto_hash import crypto_hash


def test_crypto_hash():
    assert crypto_hash(1, 2, "one") == crypto_hash("one", 2, 1)
