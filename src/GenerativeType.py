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

    def __init__(self, url, name, outdir, R, r, offset_stroke=None):
        #base_svg = download(url)
        svg_path = url
        # Radius of spectrum
        self.R = R
        # radius around sample
        self.r = r
        self.name = name
        self.outdir = outdir
        self.word = SpectrumWord(svg_path, offset_stroke)
        self.l_count = len(self.word.letters)
        if self.word.forms_count == 2:
            self.dist = "uniform"
            self.frames = 10
            self.pad = 0
        elif self.word.forms_count == 4:
            self.dist = "normal"
            self.frames = 20
        else:
            raise Exception("GenerativeType supports only 2 or 4 forms")


    def generate_animation(self, id, seed=None, transparent=True):
        np.random.seed(seed)
        C = sample_centers(self.word.forms_count, self.l_count, self.dist, self.R, self.r)
        print_drawing(self.word, C, f"{self.name}_{id}", self.outdir)
        if self.word.forms_count == 2:
            samples = sample_straight_animation(self.l_count, self.frames, self.pad, C, self.r)

        elif self.word.forms_count == 4:
            samples = sample_cirular_animation(C, self.l_count, 20, self.r)

        animate_drawing(self.word, samples, f"{self.name}_{id}", self.outdir, transparent=transparent)
        return C

    def generate_image(self, id, seed=None):
        np.random.seed(seed)
        C = sample_centers(self.word.forms_count, self.l_count, self.dist, self.R, self.r)

        print_drawing(self.word, C, self.name, self.outdir)

        return C
        # metadata = {"strokewidth" : None,
        #             "pallete" = cmap[i],
        #             "svg" = }

def main():
    configuration_path = "config.json"
    randomness_path = "randomness.json"
    input_path = "../Art/World.svg"
    name = "World"
    outdir = f"../Results/{name}"
    Path(outdir).mkdir(parents=True, exist_ok=True)

    offset_stroke = ((0, 139/255, 68/255), 5)
    transparency = False
    nft = GenerativeType(input_path, name, outdir, 1, 0.1, None)

    seed_data = json.load(open(randomness_path))
    for entry in seed_data:
        nft.generate_animation(entry["id"], entry["randomness"] % SEED_MAX, transparency)

if "__main__" == __name__:
    main()