from PIL import Image
import cairosvg
from reportlab.graphics import renderSVG, renderPM
import numpy as np
import scipy.stats as stats
import os
#TODO: Add parameters for reading speed, and letter morph speed

import math
pi = math.pi

def PointsInCircum(r,n=100):
    return [(math.cos(2*pi/n*x)*r,math.sin(2*pi/n*x)*r) for x in range(0,n+1)]

def sample_centers(forms_count, l_count, dist, R=1,r=0.1):
    dim = int(forms_count / 2)
    if dist == "normal":
        R = 1
        r = 0.1
        lower, upper = -R + r, R - r
        mu, sigma = 0, 0.7
        X = stats.truncnorm(
            (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
        C = X.rvs(size=(l_count, dim))
    elif dist == "uniform":
        C = np.random.uniform(-1, 1, size=(l_count, dim))
    return C

def sample_cirular_animation(centers,L,N,r=0.1):
    F = np.asarray(PointsInCircum(r, n=N))
    samples = np.tile(F[:,None], (L, 1))
    return samples + centers

def sample_animation_rate(L,N,P,r=0.75):
    F = np.concatenate((np.zeros(P) ,np.linspace(0,1,N), np.ones(P)))
    F = np.concatenate((F, F[::-1]))
    samples = np.tile(F, (L,1)).T
    #return samples
    samples = np.roll(samples, -P, 0)
    for i in range(L):
        # Reverse order
        #ind = L-i-1
        ind = i
        samples[:,ind] = np.roll(samples[:,ind], int(r*N/L)*i)
    return samples

def gen_frame(path):
    im = Image.open(path)
    alpha = im.getchannel('A')

    # Convert the image into P mode but only use 255 colors in the palette out of 256
    im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

    # Set all pixel values below 128 to 255 , and the rest to 0
    mask = Image.eval(alpha, lambda a: 255 if a <=128 else 0)

    # Paste the color of index 255 and use alpha as a mask
    im.paste(255, mask)

    # The transparency index is 255
    im.info['transparency'] = 255

    return im

def animate_drawing(sWord, samples, name, outdir=".", transparent=False):
    images = []
    for i, sample in enumerate(samples):
        sWord.sample(sample)
        svgfname = outdir + f"/{name}_{i}.svg"
        pngfname = outdir + f"/{name}_{i}.png"
        if transparent:
            renderSVG.drawToFile(sWord.drawing, svgfname, fmt="SVG")
            cairosvg.svg2png(url=svgfname, write_to=pngfname)
            images.append(gen_frame(pngfname))
            os.remove(svgfname)
        else:
            renderPM.drawToFile(sWord.drawing, pngfname, fmt="PNG")
            images.append(Image.open(pngfname).copy())
        os.remove(pngfname)

    images[0].save(outdir + f'/{name}.gif',
                   save_all=True,
                   format='GIF',
                   append_images=images[1:],
                   duration=80,
                   disposal=2,
                   loop=0)

