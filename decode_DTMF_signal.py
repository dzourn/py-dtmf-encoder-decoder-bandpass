import numpy as np
from scipy.io import wavfile as wav
import matplotlib.pyplot as plt
import sys

def bandpass(fs, ft, fl, fh):

    N = ft/fs
    N = 4/N
    if N%2 == 0: N+=1
    nl = nh = int(N)
    
    #low pass 
    hlpf = np.sinc(2 * fh / fs * (np.arange(nh) - (nh - 1) / 2))
    hlpf *= np.blackman(nh)
    hlpf /= np.sum(hlpf)

    #high pass
    hhpf = np.sinc(2 * fl / fs * (np.arange(nl) - (nl - 1) / 2))
    hhpf *= np.blackman(nl)
    hhpf /= np.sum(hhpf)
    hhpf = -hhpf
    hhpf[(nl - 1) // 2] += 1

    #bandpass
    return np.convolve(hlpf, hhpf)

def apply_filter(s, h):
    return np.convolve(s,h)


if len(sys.argv) != 3:
    print('USAGE: {} <signal> <number of elements>'.format(sys.argv[0]))
    exit()

rate, x = wav.read(sys.argv[1])
arr = np.array_split(x, int(sys.argv[2]))

h_low = []
h_high = []

low_band_freqs = [697, 770, 852, 941]
high_band_freqs = [1209, 1336, 1477, 1633]
fs = 8000
numbers = []

#create low band filters
for i in low_band_freqs:
    h = bandpass(8000, 80, i-20, i+20)
    h_low.append(h)

#create high band filters
for i in high_band_freqs:
    h = bandpass(8000, 80, i-20, i+20)
    h_high.append(h)

#pass number from all filters and compare
for i in arr:
    #filtered signals array
    y_low = []
    y_high = []
    
    #fft of filtered signals
    y_low_fft = []
    y_high_fft = []

    #freqs of filtered signal
    y_low_freq = []
    y_high_freq = []

    #apply low band filters and store them in array 
    for k in h_low:
        y_low.append(apply_filter(i, k))
    
    #apply high band filters and store them in array
    for k in h_high:
        y_high.append(apply_filter(i, k))
   
    #calculate low band fft
    for k in y_low:
        y_low_fft.append(np.fft.fft(k))
    
    #calculate high band fft
    for k in y_high:
        y_high_fft.append(np.fft.fft(k))

    #calculate low band freq
    for k in y_low_fft:
        y_low_freq.append(np.fft.fftfreq(len(k), 1/fs))

    #calculate high band freq
    for k in y_high_fft:
        y_high_freq.append(np.fft.fftfreq(len(k), 1/fs))

    low_mag = []
    high_mag = []
    #greatest low magnitude
    for inner in y_low_fft:
        low_mag.append(max(np.abs(inner)))
    #greatest high magnitude
    for inner in y_high_fft:
        high_mag.append(max(np.abs(inner)))

    #debug
    #print(low_mag.index(max(low_mag)))
     
    #indexes of where this mag is located (which signal "produced" it)
    index_of_low = low_mag.index(max(low_mag))
    index_of_high = high_mag.index(max(high_mag))
    
    #insufficient magnitude no number (no substansial freq)
    if max(np.abs(y_low_fft[index_of_low])) < 100 or max(np.abs(y_high_fft[index_of_high])) < 100:
            numbers.append('?')
            continue

    id_low = np.argmax(np.abs(y_low_fft[index_of_low]))
    id_high = np.argmax(np.abs(y_high_fft[index_of_high]))
    

    low_freq = abs(y_low_freq[index_of_low][id_low])
    high_freq = abs(y_high_freq[index_of_high][id_high])

    #print("{} | {}".format(low_freq, high_freq))
    
    #ugly - can be made with functions
    if (low_freq > 680 and low_freq < 700 and
        high_freq > 1190 and high_freq < 1220):
        numbers.append(1)
    elif (low_freq > 680 and low_freq < 700 and
        high_freq > 1300 and high_freq < 1350):
        numbers.append(2)
    elif (low_freq > 680 and low_freq < 700 and
        high_freq > 1460 and high_freq < 1490):
        numbers.append(3)
    elif (low_freq > 680 and low_freq < 700 and
        high_freq > 1620 and high_freq < 1650):
        numbers.append('A')
    #-----------------------------------------#
    elif (low_freq > 750 and low_freq < 790 and
        high_freq > 1190 and high_freq < 1220):
        numbers.append(4)
    elif (low_freq > 750 and low_freq < 790 and
        high_freq > 1300 and high_freq < 1350):
        numbers.append(5)
    elif (low_freq > 750 and low_freq < 790 and
        high_freq > 1460 and high_freq < 1490):
        numbers.append(6)
    elif (low_freq > 750 and low_freq < 790 and
        high_freq > 1620 and high_freq < 1650):
        numbers.append('B')
    #-----------------------------------------#
    if (low_freq > 830 and low_freq < 870 and
        high_freq > 1190 and high_freq < 1220):
        numbers.append(7)
    elif (low_freq > 830 and low_freq < 870 and
        high_freq > 1300 and high_freq < 1350):
        numbers.append(8)
    elif (low_freq > 830 and low_freq < 870 and
        high_freq > 1460 and high_freq < 1490):
        numbers.append(9)
    elif (low_freq > 830 and low_freq < 870 and
        high_freq > 1620 and high_freq < 1650):
        numbers.append('C')
    #-----------------------------------------#
    elif (low_freq > 920 and low_freq < 950 and
        high_freq > 1190 and high_freq < 1220):
        numbers.append('*')
    elif (low_freq > 920 and low_freq < 950 and
        high_freq > 1300 and high_freq < 1350):
        numbers.append(0)
    elif (low_freq > 920 and low_freq < 950 and
        high_freq > 1460 and high_freq < 1490):
        numbers.append('#')
    elif (low_freq > 920 and low_freq < 950 and
        high_freq > 1620 and high_freq < 1650):
        numbers.append('D')

print("Number found: ", end="")
for i in numbers:
    print(i,end="")
print("\n")
