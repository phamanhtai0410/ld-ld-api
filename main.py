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

@app.get("/api/staking/{campaignId}")
async def staking(campaignId: int):
    _current_active_campaign_id = 2
    _current_campaign_details = {
        "poolList": [
            {
                "campaignId": 2,
                "title": "@elonmusk",
                "image": "https://static.esollabs.com/collections/642589e3577ebbec0b002938/2023/06/17/1687015584_3bea7408-a9b5-4064-bd2a-88d0eb94982d.png",
                "name": "Elon Musk",
                "follow": "143,852,623",
                "id": "1",
                "link": "https://twitter.com/elonmusk/media",
            },
            {
                "campaignId": 2,
                "title": "@Grimezsz",
                "image": "https://static.esollabs.com/collections/642589e3577ebbec0b002938/2023/06/17/1687015649_3bbeb031-191d-423e-8256-2d77bfeb136e.png",
                "name": "Grimes",
                "follow": "2,352,623",
                "id": "2",
                "link": "https://twitter.com/Grimezsz/media",
            },
            {
                "campaignId": 2,
                "title": "@lindayacc",
                "image": "https://static.esollabs.com/collections/642589e3577ebbec0b002938/2023/06/17/1687015664_c8df8382-0f86-4a85-b1bb-fd7f5384a2ba.png",
                "name": "Linda Yaccarino",
                "follow": "32,352,623",
                "id": "3",
                "link": "https://twitter.com/lindayacc/media",
            },
            {
                "campaignId": 2,
                "title": "@xxx",
                "image": "https://static.esollabs.com/collections/642589e3577ebbec0b002938/2023/06/17/1687015678_2510fbc2-a3cf-4e74-863d-fb5389c8249d.png",
                "name": "Linda Yaccarino",
                "follow": "xx,xxx,xxx",
                "id": "4",
                "link": "https://twitter.com/xxx/media",
            }
        ]
    }
    if campaignId != _current_active_campaign_id:
        raise HTTPException(status_code=400, detail="Campaign with this ID is not available now")
    return _current_campaign_details
