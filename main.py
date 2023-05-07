import json
import os
from web3 import Web3
from redis import Redis
from fastapi import FastAPI, HTTPException

# from rediscluster import RedisCluster
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
nodes = list()
# for node in startup_nodes:
#     nodes.append(ClusterNode(host=node['host'], port=node['port']))
# print('nodes', nodes)

if os.getenv('REDIS_PASSWORD'):
    redis = Redis(host=os.getenv('REDIS_HOST'),
                  port=int(os.getenv('REDIS_PORT')),
                  password=os.getenv('REDIS_PASSWORD'))
else:
    redis = Redis(host=os.getenv('REDIS_HOST'),
                  port=int(os.getenv('REDIS_PORT')))
_web3 = Web3()

chainId = int(os.getenv('CHAIN_ID'))
airdrop_smc = os.getenv('AIRDROP_SMC', '').lower()
airdrop_smc = _web3.toChecksumAddress(airdrop_smc)


@app.get("/api/common/health_check")
async def health_check():
    return {"api": "success"}


def generate_signature(user):
    _user = _web3.toChecksumAddress(user)
    _encode = _web3.codec.encode_abi(
        [
            'uint256',
            'address',
            'address'
        ],
        [
            chainId,
            _user,
            airdrop_smc
        ]
    )
    digest = Web3.solidityKeccak(['bytes'], [f'0x{_encode.hex()}'])
    _signed_message = _web3.eth.account.signHash(
        digest,
        private_key=PRIVATE_KEY
    )

    return _signed_message.signature.hex()


@app.get("/api/airdrop/{address}")
async def airdrop(address: str):
    address = address.lower()
    _amount = redis.get(f"ladys:whitelist:{address}")
    if not _amount:
        raise HTTPException(status_code=400, detail="The address is not on the white list")

    signature = generate_signature(address)
    return {"signature": signature}
