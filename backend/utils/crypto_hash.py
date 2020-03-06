import hashlib
import json


def crypto_hash(*args):
    """
    Return a sha-256 hash of given arguments
    """
    stringified_args = sorted(map(lambda arg: json.dumps(arg), args))
    encoded_data = json.dumps("".join(stringified_args)).encode('utf-8')
    return hashlib.sha256(encoded_data).hexdigest()


if __name__ == "__main__":
    print(f"crypto hash (1, '2', [3]): {crypto_hash(1, '2', [3])}")
    print(f"crypto hash ('2', 1, [3]): {crypto_hash(1, '2', [3])}")
