import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

web3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_URL')))

abi_file = open(os.getenv('CONTRACT_ABI'))
abi = json.load(abi_file)

contract = web3.eth.contract(address = os.getenv('CONTRACT_ADDRESS'), abi = abi)
token_counter = contract.functions.tokenCounter().call()
contract_symbol = contract.functions.symbol().call()
entries = []

for id in range(token_counter):
    token_randomness = contract.functions.tokenRandomness(id).call()

    if(token_randomness != 0):
        piece_entry = {
            "id": id,
            "randomness": token_randomness
        }
        entries.append(piece_entry)

json_output = json.dumps(entries, indent=4)
    
with open(os.getenv('RANDOMNESS_FILENAME'), "w") as outfile:
    outfile.write(json_output)