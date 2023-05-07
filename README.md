# 1.env
## signer wallet private key
PRIVATE_KEY: "example"
## redis cluster host
REDIS_CLUSTER: '[{"host": "redis-cluster-example", "port": "6379"}]'
## blockchain id, eth 
CHAIN_ID: "5"
## smc airdrop (example testnet)
AIRDROP_SMC: "0x551534b6a4b249C0a22611cF3f15B45B45bE13b4"
## redis ssl option, 0 off
SSL: "0"
## redis password
REDIS_PASSWORD: "pass"


# 2. cmd
uvicorn main:app --host 0.0.0.0 --port 5005 --workers 4

