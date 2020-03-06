from backend.blockchain.block import Block, GENESIS_DATA


def test_mine_block():
    last_block = Block.genesis_block()
    data = "test=block"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash


def test_genesis_block():
    genesis = Block.genesis_block()

    assert isinstance(genesis, Block)

    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value
