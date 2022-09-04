import os
try:
    os.environ['path'] += r';C:\Program Files\UniConvertor-2.0rc5\dlls'
except:
    pass

import numpy as np
from pathlib import Path
from spectrumWord import SpectrumWord
from animation import *
from randomness import sample_centers

class GenerativeType():

    def __init__(self, url, name, outdir, R, r):
        #base_svg = download(url)
        svg_path = url
        # Radius of spectrum
        self.R = R
        # radius around sample
        self.r = r
        self.name = name
        self.outdir = outdir
        self.word = SpectrumWord(svg_path)
        self.l_count = len(self.word.P)
        if self.word.forms_count not in [2,4]:
            raise Exception("GenerativeType supports only 2 or 4 forms")
        if self.word.forms_count == 2:
            self.dist = "uniform"
        else:
            self.dist = "normal"


    def generate_animation(self, id, seed=None, transparent=True):
        np.random.seed(seed)
        C = sample_centers(self.word.forms_count, self.l_count, self.dist, self.R, self.r)
        if self.word.forms_count == 2:
            # number of morph frames
            F = 10
            # number of padding frames
            pad = 0
            samples = sample_straight_animation(self.l_count, F, pad, C, self.r)

        elif self.word.forms_count == 4:
            samples = sample_cirular_animation(C, self.l_count, 20, self.r)

        animate_drawing(self.word, samples, f"{self.name}_{id}", self.outdir, transparent=transparent)

    def generate_image(self, id, seed=None):
        np.random.seed(seed)
        C = sample_centers(self.word.forms_count, self.l_count, self.dist, self.R, self.r)
        self.word.sample(C)

        svgfname = self.outdir + f"/{self.name}_{id}.svg"
        pngfname = self.outdir + f"/{self.name}_{id}.png"
        renderSVG.drawToFile(self.word.drawing, svgfname, fmt="SVG")
        cairosvg.svg2png(url=svgfname, write_to=pngfname)
        os.remove(svgfname)

        # metadata = {"strokewidth" : None,
        #             "pallete" = cmap[i],
        #             "svg" = }

def main():
    input_path = "../Art/Rick.svg"
    name = "Rick"
    outdir = f"../Results/{name}"
    Path(outdir).mkdir(parents=True, exist_ok=True)

    nft = GenerativeType(input_path, name, outdir, 1, 0.1)
    seed = None
    for i in range(10):
        nft.generate_image(i, seed)
    for i in range(10):
        nft.generate_animation(i, seed, True)

if "__main__" == __name__:
    main()