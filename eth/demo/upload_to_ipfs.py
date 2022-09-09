from genericpath import isfile
import os
import json
import requests
from pinatapy import PinataPy
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

# Connect to the IPFS cloud service
pinata_api_key = str(os.environ.get('PINATA_API_KEY'))
pinata_secret_api_key = str(os.environ.get('PINATA_API_SECRET'))
pinata = PinataPy(pinata_api_key, pinata_secret_api_key)

output_uris = []
id = 0

while os.path.isfile(os.environ.get('INPUT_IMAGE_BASE') + str(id) + os.environ.get('IMAGE_FORMAT')):
    # upload image
    print("uploading image_" + str(id) + "...")
    image_cid = pinata.pin_file_to_ipfs(os.environ.get('INPUT_IMAGE_BASE') + str(id) + os.environ.get('IMAGE_FORMAT'))
    print("complete")

    # fetch metadata
    metadata_file = open(os.environ.get('INPUT_METADATA_BASE') + str(id) + '.json')
    metadata_json = json.load(metadata_file)

    # append the image uri
    metadata_json.update({"image": "ipfs://" + image_cid["IpfsHash"]})

    # write metadata back
    with open(os.environ.get('OUTPUT_METADATA_BASE') + str(id) + '.json', "w") as out_file:
        out_file.write(json.dumps(metadata_json, indent = 4))
    
    # upload metadata
    print("uploading metadata_" + str(id) + "...")
    metadata_cid = pinata.pin_file_to_ipfs(os.environ.get('OUTPUT_METADATA_BASE') + str(id) + ".json")
    print("complete")

    # add metadata uri to output
    output_uris.append({"id": id, "uri": "ipfs://" + metadata_cid["IpfsHash"]})

    id += 1

# write uris to output file
with open(os.environ.get('OUTPUT_URIS_FILENAME'), "w") as out_file:
    out_file.write(json.dumps(output_uris, indent = 4))
