#!/usr/bin/env python
''' Script to record soundcard output to wav file

Uses:
http://pyalsaudio.sourceforge.net/module-alsaaudio.html

to set up the sound card in a repeatable way

e.g apt-get install python-alsaaudio

You'll need and almost certainly have ``arecord`` from Debian package
``alsa-utils``.

The SVG and code inspiration for the GTK applet thing was from:

https://gitorious.org/tomate

which is under the GPL3 license.  Accordingly, so is this file, and the tomato
graphic.
'''

from os.path import join as pjoin, dirname
import sys
import shlex
from subprocess import Popen, PIPE, call
from ConfigParser import ConfigParser

import alsaaudio as aa

import pygtk
pygtk.require('2.0')
import gtk
gtk.gdk.threads_init()

MYDIR = dirname(__file__)

cfg_file = pjoin(MYDIR, 'vinyl.ini')
cfg = ConfigParser()
cfg.read(cfg_file)

WAV_DIR = cfg.get('storage', 'raw')
NX_NAME = cfg.get('card', 'name')
OUTVOLUME = int(cfg.get('card', 'outvolume'))
INVOLUME = int(cfg.get('card', 'involume'))
WAV_EXT = '.wav'

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
    cmd = 'arecord -t wav -f dat -D hw:%s %s' % (NX_NAME, fname)
    return Popen(shlex.split(cmd), stdin=PIPE, stdout=PIPE)


class LPWait(object):
    def __init__(self):
        self.icon=gtk.status_icon_new_from_file(pjoin(MYDIR, 'tomato.png'))
        self.icon.connect('activate', gtk.main_quit)
        self.icon.set_visible(True)

    def main(self):
        gtk.main()


if __name__ == '__main__':
    try:
        fname = sys.argv[1]
    except IndexError:
        raise OSError('Need filename to write to')
    if not fname.endswith(WAV_EXT):
        fname = fname + WAV_EXT
    if dirname(fname) == '':
        fname = pjoin(WAV_DIR, fname)
    # Set volumes and other things for audigy
    reset_card(OUTVOLUME, INVOLUME, NX_NAME)
    # touch output file to wake up external drive
    with open(fname, 'wb'):
        pass
    print 'Press return to start recording %s' % fname
    sys.stdin.readline()
    # Start recording
    proc = record_to(fname)
    print 'Click tomato to end'
    app = LPWait()
    try:
        app.main()
    finally:
        proc.terminate()
