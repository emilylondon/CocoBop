from scipy.io.wavfile import read
from random import randint
from numpy import fft 
import pygame, sys, time
import testStrip

file_name = 'newSong.wav'
frame_rate, amplitude = read(file_name)
frame_skip = 96
amplitude = amplitude[:, 0] + amplitude[:,1]
amplitude = amplitude[::frame_skip]
frequency = list(abs(fft.fft(amplitude)))

max_amplitude = max(amplitude)

for i in range(len(amplitude)):
    amplitude[i] = float(amplitude[i])/max_amplitude*height/4 + height/2
amplitude = [int(height/2)]*width + list(amplitude)

	#initiate graphic interface and play audio piece
pygame.init()
pygame.mixer.music.load(file_name)
pygame.mixer.music.play()
now = time.time()	

    #start visualizing!
for i in range(len(amplitude[width:])):
    if amplitude[i]>255:
        amplitude[i]=255
    audio_max=amplitude[i]