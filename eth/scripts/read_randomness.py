import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

web3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_URL')))

abi_file = open(os.getenv('CONTRACT_ABI'))
abi = json.load(abi_file)

suffix = ''

STATUS = 4
RANDOMNESS = 2

contract = web3.eth.contract(address = os.getenv('CONTRACT_ADDRESS'), abi = abi)
tokenCounter = contract.functions.tokenCounter().call()
entries = []
for id in range(tokenCounter):
    piece = contract.functions.pieceById(id).call()
    if(piece[STATUS] == 1):
        piece_entry = {
            "id": id,
            "randomness": piece[RANDOMNESS]
        }
        entries.append(piece_entry)

json_output = json.dumps(entries, indent=4)
    
with open(os.getenv('RANDOMNESS_FILENAME'), "w") as outfile:
    outfile.write(json_output)