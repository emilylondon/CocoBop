from scipy.io.wavfile import read
import numpy as np

#import pygame, sys, time
samplerate=44100
resolution=20
spwin=samplerate/resolution

#RMS for np array
def window_rms(a, window_size=2):
    energy_list = []
    for s in range(0, a.shape[0], window_size):
        e = s + window_size
        energy = np.sum(np.abs(a[s:e]**2))
        energy_list.append(energy)
    return energy_list

file_name = 'newSong.wav'
a = read(file_name)
r = np.array(a[1], dtype=float)
print(r[0])
print(r.shape)

psong=window_rms(r, window_size=int(spwin))
print(len(psong))
print(psong[900:920])
#2205 samples per window 

    #start visualizing!
