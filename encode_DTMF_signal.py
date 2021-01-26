import numpy as np
import sys
from scipy.io import wavfile as wav

DTMF_TABLE = {
    '1': [697, 1209],
    '2': [697, 1336],
    '3': [697, 1477],
    'A': [697, 1633], 

    '4': [770, 1209],
    '5': [770, 1336],
    '6': [770, 1477],
    'B': [770, 1633],

    '7': [852, 1209],
    '8': [852, 1336],
    '9': [852, 1477],
    'C': [852, 1633],

    '*': [941, 1209],
    '0': [941, 1336],
    '#': [941, 1477],
    'D': [941, 1633],
} 
 

def dtmf_encoder(number, fs):
    tone_sec = 0.5
    space_sec = 0.1
    x = np.array([])
    n = np.arange(int(tone_sec*fs))

    for num in number:
        p = np.cos(2*np.pi*(DTMF_TABLE[num][0]/fs)*n) + np.cos(2*np.pi*(DTMF_TABLE[num][1]/fs)*n) 
        space = np.zeros(int(space_sec*fs))
        x = np.concatenate((x, p, space))
    return x

if len(sys.argv) != 2:
    print('USAGE: {} <number>'.format(sys.argv[0]))
    exit()

fs = 8000 #8khz sampling frequency

x = dtmf_encoder(sys.argv[1], fs)
wav.write('my_number.wav',  fs, x.astype(np.float32))

