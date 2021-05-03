from scipy.io.wavfile import read
import numpy as np

#import pygame, sys, time
samplerate=44100
resolution=20
spwin=samplerate/resolution

#RMS for np array
def window_rms(a, window_size=2):
    return np.sqrt(sum([a[window_size-i-1:len(a)-i]**2 for i in range(window_size-1)])/window_size)

file_name = 'newSong.wav'
a = read(file_name)
r = np.array(a[1], dtype=float)
print(r[0])
print(r.shape)

psong=window_rms(r, window_size=int(spwin))
print(psong.shape)
print(psong[2000:2020])
#2205 samples per window 

    #start visualizing!
