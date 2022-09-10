import os
import shutil
import json
from web3 import Web3
from dotenv import load_dotenv
from GenerativeType import generateArtFromArray
from pathlib import Path
from pinatapy import PinataPy
import requests
from genericpath import isfile

load_dotenv()

class UriGenerator:
    # contracts_filename should is the path to a json file containing an array of {symbol: , address: }
    def __init__(self, address_book = "./contracts/address_book.json"):
        print('connecting to Infura...')
        self.web3 = Web3(Web3.HTTPProvider(os.getenv('INFURA_URL')))
        self.contracts = json.load(open(address_book)

        print('connecting to Pinata...')
        self.pinata = PinataPy(str(os.environ.get('PINATA_API_KEY')), str(os.environ.get('PINATA_API_SECRET')))
    
    def generate(self):
        for contract_entry in self.contracts:
            print("=== contract " + contract_entry["symbol"] + " at address " + contract_entry["address"] + " ===")
            contract_path = "./contracts/" + contract_entry["symbol"] + "/"
            contract_abi = json.load(open(contract_path + "abi.json"))
            contract = self.web3.eth.contract(address = contract_entry["address"], abi = contract_abi)
                        
            randomness = self.readRandomnessFromContract(contract)

            output_dir = self.makeOutputDir(contract_path)

            generateArtFromArray(randomness, contract_path + "media", contract_path + 'config.json', output_dir)

            uris = self.uploadToIPFS(output_dir)
            # write uris to output file
            
            print("writing output file...")
            with open(contract_path + "results/uris.json", "w") as out_file:
                out_file.write(json.dumps(uris, indent = 4))

    def readRandomnessFromContract(self, contract):
        token_counter = contract.functions.tokenCounter().call()
        entries = []
        print("reading randomness...")
        # read randomness from contract
        for id in range(token_counter):
            token_randomness = contract.functions.tokenRandomness(id).call()

            if(token_randomness != 0):
                piece_entry = {
                    "id": id,
                    "randomness": token_randomness
                }
                entries.append(piece_entry)

        print("collected randomness for " + str(len(entries)) + " tokens out of " + str(token_counter))
        
        return entries

    def makeOutputDir(self, contract_path):
        print('creating output directory...')
        output_dir = contract_path + "output"
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        return output_dir

    def uploadToIPFS(self, results_dir):
        output_uris = []
        id = 0

        # copy files to directory           
        file_names = os.listdir(results_dir)
        for file_name in file_names:
            shutil.move(os.path.join(results_dir, file_name), ".")

        while os.path.isfile(os.environ.get('IMAGE_PREFIX') + str(id) + os.environ.get('IMAGE_FORMAT')):

            # upload image
            print("uploading image for token " + str(id) + " to ipfs...")
            image_cid = self.pinata.pin_file_to_ipfs(os.environ.get('IMAGE_PREFIX') + str(id) + os.environ.get('IMAGE_FORMAT'))
            print("complete")

            # fetch metadata
            metadata_file = open(os.environ.get('METADATA_PREFIX') + str(id) + '.json')
            metadata_json = json.load(metadata_file)

            # append the image uri
            metadata_json.update({"image": "ipfs://" + image_cid["IpfsHash"]})

            # write metadata back
            with open(os.environ.get('METADATA_PREFIX') + str(id) + '.json', "w") as out_file:
                out_file.write(json.dumps(metadata_json, indent = 4))
            
            # upload metadata
            print("uploading metadata for token " + str(id) + " to ipfs...")
            metadata_cid = self.pinata.pin_file_to_ipfs(os.environ.get('METADATA_PREFIX') + str(id) + ".json")
            print("complete")

            # add metadata uri to output
            output_uris.append({"id": id, "uri": "ipfs://" + metadata_cid["IpfsHash"]})

            id += 1

            out_file.close()

        #for file_name in file_names:
        #    shutil.move(file_name, results_dir)

        return output_uris

def main():
    UriGenerator().generate()
                










    




