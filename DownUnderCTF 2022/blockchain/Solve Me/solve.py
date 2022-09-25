import web3
import json
from solcx import compile_standard, install_solc
from web3.middleware import geth_poa_middleware


ENDPOINT_ADDR = "https://blockchain-solveme-################-eth.2022.ductf.dev/"
CONTRACT_ADDR = "0x6E4198C61C75D1B4D1cbcd00################"
PLAYER_ADDR = "0x8460dA1D1803988fECdB8710################"
PRIVATE_KEY = "0x17f82be4c843c20f157ac0db2421e6968a5e69a557471f48################"
CHAIN_ID = 31337

# <----------------------------------------------------ABI------------------------------------------------------>
with open("SolveMe.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.8.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SolveMe.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

abi = json.loads(compiled_sol["contracts"]["SolveMe.sol"]["SolveMe"]["metadata"])["output"]["abi"]
# <----------------------------------------------------ABI------------------------------------------------------>

w3 = web3.Web3(web3.Web3.HTTPProvider(ENDPOINT_ADDR))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)  # Fix

contr = w3.eth.contract(address=CONTRACT_ADDR, abi=abi)
contr_tx = contr.functions.solveChallenge().buildTransaction(
    {
        "chainId": CHAIN_ID,
        'from': PLAYER_ADDR,
        'nonce': w3.eth.get_transaction_count(PLAYER_ADDR),
        "gasPrice": w3.eth.gas_price  # Fix
    }
)

tx_create = w3.eth.account.signTransaction(contr_tx, PRIVATE_KEY)
tx_hash = w3.eth.sendRawTransaction(tx_create.rawTransaction)

