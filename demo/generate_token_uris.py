import os
import json
from web3 import Web3
from dotenv import load_dotenv
from GenerativeType import generateArtFromArray
from pathlib import Path

load_dotenv()

class UriGenerator:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_URL')))      
    
    def generateUris(self, contract_address, abi_path):
        abi = json.load(abi_path)
        contract = self.web3.eth.contract(address = contract_address, abi = abi)
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

        output_dir = f"../output/" + contract_symbol
        Path(output_dir).mkdir(parents=True, exist_ok=True)

        generateArtFromArray(entries, os.getenv('CONFIG_PATH') + contract_symbol + '.json', output_dir)        










    




