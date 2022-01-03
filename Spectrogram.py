import os
from subprocess import check_call
from tempfile import mktemp
# from scikits.audiolab import wavread, play
import soundfile
from scipy.signal import remez, lfilter
from pylab import *
import itertools
import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--feed', required=True, help='path to folder with small clips')
parser.add_argument('-o', '--output', default="spectrogram", help='output path for spectrograms')
parser.add_argument('--avconv', default="libav/bin/avconv", help='custom avconv binary location')
opt = parser.parse_args()
print(opt)

for i in itertools.count():

    # convert mp3, read wav
    try:
        mp3filename = opt.feed+"/clip{0}.mp3".format(i)
        wname = mktemp('.wav')
        check_call([opt.avconv, '-i', mp3filename, wname])
        sig, fs = soundfile.read(wname)
        os.unlink(wname)
    except:
        print("All spectrograms created.")
        exit(0)

    # bandpass filter
    bands = array([0, 3500, 4000, 5000, 5500, fs/2.0]) / fs  # change this
    desired = [0, 1, 0]
    b = remez(513, bands, desired)
    sig_filter = lfilter(b, 1, sig)

    sig_filter /= 1.05 * np.amax((abs(sig_filter)), axis=0)  # normalize

    # Plotting normal spectrogram
    # subplot(211)
    # specgram(sig.flatten(), Fs=fs, NFFT=1024, noverlap=0)
    # axis('tight'); axis(ymax=6000)
    # title('Original')

    # Plotting filtered spectrogram
    # subplot(212)
    # specgram(sig_filter.flatten(), Fs=fs, NFFT=1024, noverlap=0)
    # axis('tight'); axis(ymax=6000)
    # title('Filtered')

    #Saving spectrogram to png
    if not os.path.exists(opt.output):
        os.makedirs(opt.output)

    fig, ax = subplots(1)
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.axis('off')
    ax.specgram(sig.flatten(), Fs=fs, NFFT=1024, noverlap=384)
    ax.axis('off')
    fig.savefig(opt.output+'/sp{0}.png'.format(i), dpi=300, frameon='false')
