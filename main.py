import json
import os
from web3 import Web3
from redis.cluster import RedisCluster, ClusterNode
from fastapi import FastAPI, HTTPException

# from rediscluster import RedisCluster
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

startup_nodes = json.loads(os.getenv('REDIS_CLUSTER', '[]'))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
nodes = list()
for node in startup_nodes:
    nodes.append(ClusterNode(host=node['host'], port=node['port']))
print('nodes', nodes)

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
_web3 = Web3()

chainId = int(os.getenv('CHAIN_ID'))
airdrop_smc = os.getenv('AIRDROP_SMC', '').lower()
airdrop_smc = _web3.toChecksumAddress(airdrop_smc)

@app.get("api/common/health_check")
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


@app.get("api/airdrop/{address}")
async def airdrop(address: str):
    address = address.lower()
    _amount = redis.get(f"ladys:whitelist:{address}")
    if not _amount:
        raise HTTPException(status_code=400, detail="The address is not on the white list")

    signature = generate_signature(address)
    return {"signature": signature}