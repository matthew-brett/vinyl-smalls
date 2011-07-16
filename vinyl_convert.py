#!/usr/bin/env python
""" Converts wav files from audigy

Needs sox

e.g apt-get install sox
"""

import os
import sys
import subprocess

# Directory where raw files etc have gone
root_dir = '/media/ntb/vinyl'
wav_sdir='raw'
wav_441_sdir='wav_441'

wav_dir = os.path.join(root_dir, wav_sdir)
wav_441_dir = os.path.join(root_dir, wav_441_sdir)

if not os.path.exists(wav_441_dir):
    os.mkdir(wav_441_dir)

# Convert argv passed filenames
for arg in sys.argv[1:]:
    path, fname = os.path.split(arg)
    i_fname = os.path.join(wav_dir, fname)
    c_fname = os.path.join(wav_441_dir, fname)
    exec_str = 'sox %s -r 44100 %s resample -ql' % (i_fname, c_fname)
    print exec_str
    subprocess.call(exec_str, shell=True)
