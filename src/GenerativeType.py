import os
try:
    os.environ['path'] += r';C:\Program Files\UniConvertor-2.0rc5\dlls'
except:
    pass

import numpy as np
from pathlib import Path
from spectrumWord import SpectrumWord
from animation import *
import random

SEED_LOWER_BOUND = 0
SEED_UPPER_BOUND = 2**20

class GenerativeType():

    def __init__(self, url, name, outdir):
        #base_svg = download(url)
        svg_path = url
        self.name = name
        self.outdir = outdir
        self.word = SpectrumWord(svg_path)
        self.l_count = len(self.word.P)
        if self.word.forms_count not in [2,4]:
            raise Exception("GenerativeType supports only 2 or 4 forms")

    def sample_image(self, seed):
        locs = np.rand(seed % self.N, (self.word.P,), (0, 1))
        image = self.word.sample(locs)
        return image

    def generate_animation(self, seed, method, transparent=True):
        R = 1
        r = 0.2
        if method == "straight":
            C = sample_centers(self.word.forms_count, self.l_count, "uniform", R, r)
            # number of morph frames
            F = 10
            # number of padding frames
            pad = 0
            samples = sample_straight_animation(self.l_count, F, pad, C, r)

        elif method == "circular":
            C = sample_centers(self.word.forms_count, self.l_count, "normal")
            samples = sample_cirular_animation(C, self.l_count, 20)

        animate_drawing(self.word, samples, f"{self.name}_{seed}", self.outdir, transparent=transparent)

    def generate_image(self, seed=None, dist="normal"):
        C = sample_centers(self.word.forms_count, self.l_count, "normal")
        self.word.sample(C)

        svgfname = self.outdir + f"/{self.name}_{seed}.svg"
        pngfname = self.outdir + f"/{self.name}_{seed}.png"
        renderSVG.drawToFile(self.word.drawing, svgfname, fmt="SVG")
        cairosvg.svg2png(url=svgfname, write_to=pngfname)
        os.remove(svgfname)

        # metadata = {"strokewidth" : None,
        #             "pallete" = cmap[i],
        #             "svg" = }

def main():
    input_path = "../Art/world.svg"
    name = "World"
    outdir = f"../Results/{name}"
    Path(outdir).mkdir(parents=True, exist_ok=True)

    nft = GenerativeType(input_path, name, outdir)

    for i in range(0):
        nft.generate_image(i)
    for i in range(20):
        nft.generate_animation(i, "straight", False)
    #nft.generate(seed=4536789)

if "__main__" == __name__:
    main()