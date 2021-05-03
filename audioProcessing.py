from scipy.io.wavfile import read
import numpy as np
#import pygame, sys, time

file_name = 'newSong.wav'
a = read(file_name)
r = np.array(a[1], dtype=float)
print(r[0])
print(r.shape)

	#initiate graphic interface and play audio piece


    #start visualizing!
