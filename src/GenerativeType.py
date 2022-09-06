import os
try:
    os.environ['path'] += r';C:\Program Files\UniConvertor-2.0rc5\dlls'
except:
    pass

import json
import numpy as np
from pathlib import Path
from spectrumWord import SpectrumWord
from animation import *
from randomness import sample_centers

SEED_MAX = 2**32 - 1

class GenerativeType():

    def __init__(self, config):
        # Offset stroke
        os_color = np.asarray(config["os_color"])/ 255
        os_width = config["os_width"]
        offset_stroke = (os_color, os_width) if os_width > 0 else None

        self.word = SpectrumWord(config["svg_path"], offset_stroke)
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

        self.name = config["name"]
        self.outdir = f"../Results/{self.name}"
        Path(self.outdir).mkdir(parents=True, exist_ok=True)


    def generate(self, id, seed=None):
        np.random.seed(seed)
        C = sample_centers(self.word.forms_count, self.l_count, self.dist, self.R, self.r)
        print_drawing(self.word, C, f"{self.name}_{id}", self.outdir)
        if self.word.forms_count == 2:
            samples = sample_straight_animation(C, self.l_count, self.frames_count, self.pad, self.r)

        elif self.word.forms_count == 4:
            samples = sample_cirular_animation(C, self.l_count, self.frames_count, self.r)

        animate_drawing(self.word, samples, f"{self.name}_{id}", self.outdir, transparent=self.transparency)
        return C

        # metadata = {"strokewidth" : None,
        #             "pallete" = cmap[i],
        #             "svg" = }

def main():
    configuration_path = "config.json"
    config = json.load(open(configuration_path))

    nft = GenerativeType(config)

    seed_data = json.load(open(config["randomness_path"]))
    for entry in seed_data:
        C = nft.generate(entry["id"], entry["randomness"] % SEED_MAX)


if "__main__" == __name__:
    main()