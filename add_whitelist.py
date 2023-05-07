import json
import os

from web3 import Web3
from dotenv import load_dotenv
from redis import Redis
import csv

load_dotenv()

if os.getenv('REDIS_PASSWORD'):
    redis = Redis(host=os.getenv('REDIS_HOST'),
                  port=int(os.getenv('REDIS_PORT')),
                  password=os.getenv('REDIS_PASSWORD'))
else:
    redis = Redis(host=os.getenv('REDIS_HOST'),
                  port=int(os.getenv('REDIS_PORT')))
# address = "0x40469BdF7De2a67fE4138D248dbdfa5585F8937B".lower()
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

    print(f'Processed {line_count - 1} lines. Done: {done_address} Error: {fail_address}')
