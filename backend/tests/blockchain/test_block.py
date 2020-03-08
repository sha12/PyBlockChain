from backend.blockchain.block import Block, GENESIS_DATA
import time
from backend.config import MINE_RATE, SECONDS
from backend.utils.hex_to_binary import hex_to_binary
import pytest


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


def test_is_block_valid():
    last_block = Block.genesis_block()
    block = Block.mine_block(last_block, "dummy data")
    Block.is_block_valid(last_block, block)

    # bad last hash check
    block = Block.mine_block(last_block, "dummy data")
    block.last_hash = "evil_last_hash"
    with pytest.raises(Exception, match="The last block hash and the last hash of the new block should match"):
        Block.is_block_valid(last_block, block)

    # bad proof of work
    block = Block.mine_block(last_block, "dummy data")
    block.hash = "aaaaa"
    with pytest.raises(Exception, match="Proof of work requirement not met"):
        Block.is_block_valid(last_block, block)

    # difficulty tampered
    difficulty = 10
    block = Block.mine_block(last_block, "dummy data")
    block.difficulty = difficulty
    block.hash = f"{'0' * difficulty}1111a"

    with pytest.raises(Exception, match="The block difficulty must only adjust by 1"):
        Block.is_block_valid(last_block, block)
