from backend.blockchain.block import Block, GENESIS_DATA
import time
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_binary


def test_mine_block():
    last_block = Block.genesis_block()
    data = "test=block"
    block = Block.mine_block(last_block, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.last_hash == last_block.hash
    assert hex_to_binary(block.hash)[
        0:block.difficulty] == '0'*block.difficulty


def test_genesis_block():
    genesis = Block.genesis_block()

    assert isinstance(genesis, Block)

    for key, value in GENESIS_DATA.items():
        getattr(genesis, key) == value


def test_quickly_mined_block():
    last_block = Block.mine_block(Block.genesis_block(), 'abcd')
    mined_block = Block.mine_block(last_block, '1234')

    assert mined_block.difficulty == last_block.difficulty + 1


def test_slowly_mined_block():
    last_block = Block.mine_block(Block.genesis_block(), 'abcd')
    time.sleep(MINE_RATE/SECONDS)
    mined_block = Block.mine_block(last_block, '1234')
    assert mined_block.difficulty == last_block.difficulty - 1


def test_difficulty_limit_at_1():
    last_block = Block(
        time.time_ns(),
        'last_hash',
        'test_hash',
        'test_data',
        1,
        0
    )
    time.sleep(MINE_RATE / SECONDS)
    mined_block = Block.mine_block(last_block, "Dummy data")
    assert mined_block.difficulty == 1
