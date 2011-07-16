#!/usr/bin/env python
''' Script to record soundcard to wav file
Uses:
http://pyalsaudio.sourceforge.net/module-alsaaudio.html

to set up the sound card in a repeatable way

e.g apt-get install python-alsaaudio
'''

import os
import sys
import shlex
from subprocess import Popen, PIPE, call

import alsaaudio as aa

default_path = '/media/ntb/vinyl/raw'
nx_name = 'NX' # alsa card name for NX
wav_ext = '.wav'
outvolume = 92
involume = 92

def card_index(name):
    cards = aa.cards()
    if not name in cards:
        raise RuntimeError('Cannot find card "%s"' % name)
    return aa.cards().index(name)


def reset_card(outvolume, involume, name):
    nx_no = card_index(name)
    mxr = aa.Mixer('Master', cardindex=nx_no)
    mxr.setvolume(outvolume)
    mxr.setmute(0)
    mxr = aa.Mixer('Line', cardindex=nx_no)
    mxr.setvolume(outvolume)
    mxr.setmute(0)
    mxr.setvolume(involume, 0, 'capture')


def record_to(fname):
    cmd = 'arecord -t wav -f dat -D hw:%s %s' % (nx_name, fname)
    return Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE)


if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        raise OSError('Need filename to write to')
    if not fname.endswith(wav_ext):
        fname = fname + wav_ext
    if not os.path.isabs(fname):
        fname = os.path.join(default_path, fname)
    # Set volumes and other things for audigy
    reset_card(outvolume, involume, nx_name)
    # touch output file to wake up external drive
    retcode = call('touch %s' % fname, shell=True)
    print 'Press return to start recording %s' % fname
    sys.stdin.readline()
    # Start recording
    proc = record_to(fname)
    print 'Press return to end'
    # Catch keyboard interrupts to kill recording
    try:
        sys.stdin.readline()
    finally: # catches keyboard interrupt as well as keypress
        proc.terminate()
