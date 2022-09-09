import json
from pathlib import Path
from spectrumWord import SpectrumWord
from animation import *
from randomness import sample_centers

SEED_MAX = 2**32 - 1


class GenerativeType:

    def __init__(self, config):
        # Offset stroke
        os_color = np.asarray(config["os_color"])/ 255
        os_width = config["os_width"]
        offset_stroke = (os_color, os_width) if os_width > 0 else None
        self.name = config["name"]
        self.input_path = os.path.join("..", "media", self.name)
        self.word = SpectrumWord(f"{self.input_path}/{self.name}.svg", self.input_path, offset_stroke)
        self.l_count = len(self.word.letters)

        self.frames_count = config["frames"]
        if self.word.forms_count == 2:
            self.dist = "uniform"
            self.frames_count //= 2
            self.pad = 0
        elif self.word.forms_count == 4:
            self.dist = "normal"
        else:
            raise Exception("GenerativeType supports only 2 or 4 forms")

        # Radius of spectrum, radius around sample
        self.R, self.r = config["R"], config["r"]

        self.transparency = config["transparency"]

        self.bg_images = config["background_images"]
        self.bg_descriptions = config["background_descriptions"]

        self.outdir = f"../Results/{self.name}"
        Path(self.outdir).mkdir(parents=True, exist_ok=True)


    def generate(self, id, seed=None):
        np.random.seed(seed)
        self.word.set_background_image(self.bg_images, self.bg_descriptions)

        C = sample_centers(self.word.forms_count, self.l_count, self.dist, self.R, self.r)
        print_drawing(self.word, C, f"{self.name}_{id}", self.outdir)
        if self.word.forms_count == 2:
            samples = sample_straight_animation(C, self.l_count, self.frames_count, self.pad, self.r)

        elif self.word.forms_count == 4:
            samples = sample_cirular_animation(C, self.l_count, self.frames_count, self.r)

        animate_drawing(self.word, samples, f"{self.name}_{id}", self.outdir, transparent=self.transparency)
        return self.word.calculate_ar_heb_percentages(C)

        # metadata = {"strokewidth" : None,
        #             "pallete" = cmap[i],
        #             "svg" = }

def generate_metadata_file(config, ar_heb_percentages, background_image):
    ar_percentage, heb_percentage = ar_heb_percentages
    metadata = {
        "description" : config["description"],
        "background_color" : config["background_color"],
        "attributes" : [
            {
                "display_type" : "boost_percentage",
                "trait_type" : "Hebrew",
                "value" : heb_percentage
            },
            {
                "display_type" : "boost_percentage",
                "trait_type" : "Arabic",
                "value" : ar_percentage
            },
            {
                "trait_type" : "Background",
                "value" :  background_image
            }
        ]
    }
    return metadata

def test():
    configuration_path = "config.json"
    config = json.load(open(configuration_path))

    nft = GenerativeType(config)

    for i in range(20):
        ar_heb = nft.generate(i, None)
        metadata_path = f"{nft.outdir}/metadata_{i}.json"
        metadata = generate_metadata_file(config, ar_heb, nft.word.bg_description)
        json.dump(metadata, open(metadata_path, 'w'))

def generateArtFromArray(randomness_entries):
    art_config = json.load(open(configuration_path))
    generative_module = GenerativeType(art_config)
    for entry in randomness_entries:
        ar_heb = generative_module.generate(entry["id"], entry["randomness"] % SEED_MAX)
        metadata_path = f"{generative_module.outdir}/metadata_{entry['id']}.json"
        metadata = generate_metadata_file(art_config, ar_heb, generative_module.word.bg_description)
        json.dump(metadata, open(metadata_path, 'w'))


def main():
    configuration_path = "config.json"
    config = json.load(open(configuration_path))

    nft = GenerativeType(config)

    seed_data = json.load(open(config["randomness_path"]))
    for entry in seed_data:
        ar_heb = nft.generate(entry["id"], entry["randomness"] % SEED_MAX)
        metadata_path = f"{nft.outdir}/metadata_{entry['id']}.json"
        metadata = generate_metadata_file(config, ar_heb, nft.word.bg_description)
        json.dump(metadata, open(metadata_path, 'w'))

if "__main__" == __name__:
    test()