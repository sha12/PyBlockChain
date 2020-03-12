from backend.blockchain.blockchain import BlockChain
import time
from backend.config import SECONDS

blockchain = BlockChain()

times = []

for i in range(100):
    start_time = time.time_ns()
    blockchain.add_block(i)
    time_to_mine = (time.time_ns() - start_time) / SECONDS
    times.append(time_to_mine)
    print(f"Time to mine: {time_to_mine}")
    print(f"Difficulty of the block: {blockchain.chain[-1].difficulty}")
    print(f"Average time to mine: {sum(times)/len(times)}")

print(sum(times) / len(times))
