import json
import os

from dotenv import load_dotenv
from rediscluster import RedisCluster

load_dotenv()

startup_nodes = json.loads(os.getenv('REDIS_CLUSTER', '[]'))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

redis = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)
address = "0x5146966039EEc18E65Ae6443723e8C2366A40c79".lower()
redis.set(f"ladys:whitelist:{address}", 1)
