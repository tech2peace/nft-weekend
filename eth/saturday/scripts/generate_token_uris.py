import os
import json
from web3 import Web3
from dotenv import load_dotenv
from DIRECTORY import generateArtFromArray
load_dotenv()

web3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_URL')))

abi = json.load(open(os.getenv('CONTRACT_ABI')))

contract = web3.eth.contract(address = os.getenv('CONTRACT_ADDRESS'), abi = abi)
token_counter = contract.functions.tokenCounter().call()
contract_symbol = contract.functions.symbol().call()
entries = []

# read randomness from contract
for id in range(token_counter):
    token_randomness = contract.functions.tokenRandomness(id).call()

    if(token_randomness != 0):
        piece_entry = {
            "id": id,
            "randomness": token_randomness
        }
        entries.append(piece_entry)

generateArtFromArray(entries, os.getenv('OUTPUT_DIR'))




