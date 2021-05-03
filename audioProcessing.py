from scipy.io import wavfile 
import pygame, sys, time
import testStrip

file_name = 'newSong.wav'
sample_rate, amplitude = wavfile.read(file_name)
print(sample_rate)
print(amplitude)

	#initiate graphic interface and play audio piece
pygame.init()
pygame.mixer.music.load(file_name)
pygame.mixer.music.play()
now = time.time()	

    #start visualizing!
