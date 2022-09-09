import json

input_base = '../input/metadata/metadata_'
output_base = '../output/metadata/metadata_'

input_file = open('../samples/uris.txt', 'r')
lines = input_file.readlines()

id = 0

# Strips the newline character
for line in lines:
    # read metadata
    metadata_file = open(input_base + str(id) + '.json')
    metadata_json = json.load(metadata_file)
  
    # append the image uri
    metadata_json.update({"image": line.strip()})
 
    # write metadata back
    with open(output_base + str(id) + '.json', "w") as out_file:
        out_file.write(json.dumps(metadata_json, indent = 4))
    id += 1
