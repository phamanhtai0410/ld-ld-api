import json
import os
from web3 import Web3

from fastapi import FastAPI, HTTPException

from rediscluster import RedisCluster
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

startup_nodes = json.loads(os.getenv('REDIS_CLUSTER', '[]'))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

redis = RedisCluster(startup_nodes=startup_nodes, decode_responses=True,skip_full_coverage_check=True)
_web3 = Web3()

chainId = int(os.getenv('CHAIN_ID'))
airdrop_smc = os.getenv('AIRDROP_SMC', '').lower()
airdrop_smc = _web3.toChecksumAddress(airdrop_smc)

@app.get("/common/health_check")
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


@app.get("/airdrop/{address}")
async def airdrop(address: str):
    address = address.lower()
    _amount = redis.get(f"ladys:whitelist:{address}")
    if not _amount:
        raise HTTPException(status_code=400, detail="The address is not on the white list")

    signature = generate_signature(address)
    return {"signature": signature}
