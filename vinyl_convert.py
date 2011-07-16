#!/usr/bin/env python
""" Converts wav files from 4800 Hz to 44100 Hz

Needs sox

e.g apt-get install sox
"""

import os
from os.path import (dirname, join as pjoin, exists, 
                     split as psplit)
import sys
import subprocess
from ConfigParser import ConfigParser

cfg_file = pjoin(dirname(__file__), 'vinyl.ini')
cfg = ConfigParser()
cfg.read(cfg_file)

wav_dir = cfg.get('storage', 'raw')
wav_441_dir = cfg.get('storage', 'cd')

if not exists(wav_441_dir):
    os.mkdir(wav_441_dir)

# Convert argv passed filenames
for arg in sys.argv[1:]:
    path, fname = psplit(arg)
    if path == '':
        path = wav_dir
    i_fname = pjoin(path, fname)
    c_fname = pjoin(wav_441_dir, fname)
    exec_str = 'sox %s -r 44100 %s resample -ql' % (i_fname, c_fname)
    print exec_str
    subprocess.call(exec_str, shell=True)

