import json
import os

from web3 import Web3
from dotenv import load_dotenv
from redis.cluster import RedisCluster, ClusterNode
import csv

load_dotenv()

startup_nodes = json.loads(os.getenv('REDIS_CLUSTER', '[]'))
nodes = list()
for node in startup_nodes:
    nodes.append(ClusterNode(host=node['host'], port=node['port']))

if os.getenv('REDIS_PASSWORD'):
    ssl_redis = bool(int(os.getenv("SSL", "0")))
    print('ssl', ssl_redis)
    redis = RedisCluster(startup_nodes=nodes,
                         # host=os.getenv("REDIS_AUTH_HOST"),
                         # port=int(os.getenv("REDIS_AUTH_PORT")),
                         decode_responses=True,
                         ssl=ssl_redis,
                         skip_full_coverage_check=True,
                         password=os.getenv('REDIS_PASSWORD'))
else:
    redis = RedisCluster(startup_nodes=nodes,
                         decode_responses=True,
                         skip_full_coverage_check=True)

# address = "0x183Ff214179cd2B1c06A937D663F192340edd159".lower()
# redis.set(f"ladys:whitelist:{address}", 1)
_web3 = Web3()
with open('whitelist_holder.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    done_address = 0
    fail_address = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            address = row[0].lower().replace(" ", "")
            if _web3.isAddress(address):
                redis.set(f"ladys:whitelist:{address}", 1)
                done_address += 1
                print(f'\t{row[0]} .... done')
            else:
                fail_address += 1
                print(f'\t{row[0]} .... is not a address')
            line_count += 1

    print(f'Processed {line_count-1} lines. Done: {done_address} Error: {fail_address}')
