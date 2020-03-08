from backend.utils.hex_to_binary import hex_to_binary


def test_hex_to_binary():
    num = 164
    binary = hex_to_binary(hex(num)[2:])
    assert num == int(binary, 2)
