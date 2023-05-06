import json
import os

from web3 import Web3
from dotenv import load_dotenv
from rediscluster import RedisCluster
import csv

load_dotenv()

startup_nodes = json.loads(os.getenv('REDIS_CLUSTER', '[]'))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

redis = RedisCluster(startup_nodes=startup_nodes, decode_responses=True, skip_full_coverage_check=True)

_web3 = Web3()
with open('whitelist.csv') as csv_file:
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
