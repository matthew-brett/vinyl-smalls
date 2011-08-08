""" Script to process set of photos of LPs

Specific to these photos
"""

import os
from os.path import (dirname, join as pjoin, exists, 
                     split as psplit)
import sys
import subprocess
from ConfigParser import ConfigParser

import numpy as np

# PIL
import Image
from PIL.ImageOps import autocontrast

# Location of files
cfg_file = pjoin(dirname(__file__), 'vinyl.ini')
cfg = ConfigParser()
cfg.read(cfg_file)
img_dir = cfg.get('storage', 'art')

Y = (315, 1515)
X = (58, 1260)
PCT_DROP = 5

for froot in os.listdir(img_dir):
    in_fname = pjoin(img_dir, froot)
    out_fname = pjoin(img_dir, 'c_' + froot)
    img = Image.open(in_fname)
    c_img = autocontrast(img, PCT_DROP)
    arr = np.array(c_img)
    arr = arr[X[0]:X[1], Y[0]:Y[1]]
    out_img = Image.fromarray(arr)
    out_img.save(out_fname)

