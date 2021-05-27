from scipy.io.wavfile import read
import numpy as np
import time
import threading
import logging
import pigpio
import os
import sys
from pigpio_encoder import pigpio_encoder

#sys.path.append('/home/pi/Dexter/GrovePi/Software/Python')
#import grovepi
#set up input pins for rotary encoder and LED pins

RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24
CLK = 18
DT = 4

#Brightness Values for RGB, make them global so they can be modified across threads

RED=255
GREEN = 0
BLUE = 0 
flag = 0

#Set up LED, initialize to red 

pi = pigpio.pi()
pi.set_PWM_dutycycle(RED_PIN, RED)
pi.set_PWM_dutycycle(BLUE_PIN, BLUE)
pi.set_PWM_dutycycle(GREEN_PIN, GREEN)


def color_map(amp, color):
    mapped = color*(amp/9000)
    if mapped > 255:
        mapped = 255
    return mapped 

#set up audio processing parameters

samplerate=44100
resolution=20
spwin=samplerate/resolution
        
 #color cycle thread    
def color_cycle():
    global flag
    global RED
    global BLUE
    global GREEN
    if flag == 0:
        RED = 255
        GREEN = 0
        BLUE = 0
        while flag == 0: 
            for g in range(255):
                GREEN = g
                time.sleep(0.05)
            for r in range(255, 0, -1):
                RED = r
                time.sleep(0.05)
            for b in range(255):
                BLUE = b
                time.sleep(0.05)
            for gr in range(255, 0, -1):
                GREEN = gr 
                time.sleep(0.05)
            for re in range(255):
                RED = re
                time.sleep(0.05)
            for bl in range(255, 0, -1):
                BLUE = bl
                time.sleep(0.05)

#Thread for music player
def music_player():
    logging.info("Playing song now")
    os.system("omxplayer " + "newSong.wav")
    logging.info("Song done")
    pi.set_PWM_dutycycle(RED_PIN, 0)
    pi.set_PWM_dutycycle(GREEN_PIN, 0)
    pi.set_PWM_dutycycle(BLUE_PIN, 0)

#Visualization thread
def audio_visualizer(psong, pcolors):
    logging.info("Visualizing audio")
    time.sleep(1)
    global RED
    global BLUE 
    global GREEN
  
    for t in range(len(psong)):
        r = color_map(psong[t], RED)
        g = color_map(psong[t], GREEN)
        b = color_map(psong[t], BLUE)
        pi.set_PWM_dutycycle(RED_PIN, r)
        pi.set_PWM_dutycycle(GREEN_PIN, g)
        pi.set_PWM_dutycycle(BLUE_PIN, b)
        print(pcolors[t].shape)
        time.sleep(0.05)
    logging.info("Song over")


#function for RMS 
def window_rms(a, window_size=2):
    energy_list = []
    color_fft_list = []
    for s in range(0, a.shape[0], window_size):
        e = s + window_size
        #energy = np.sum(np.abs(a[s:e]**2))
        energy = np.sqrt(np.mean(a[s:e]**2))
        color = np.fft.fft(a)
        energy_list.append(energy)
        color_fft_list.append(color)
    return energy_list, color_fft_list
#read in file
file_name = 'newSong.wav'
print("File downloaded and loaded in")
a = read(file_name)
r = np.array(a[1], dtype=float)
print(r[0])
print(r.shape)
#2205 samples per window 
psong, pcolors=window_rms(r, window_size=int(spwin))
#start visualizing!
if __name__ == "__main__":
    t0 = threading.Thread(target=music_player)
    t1 = threading.Thread(target=audio_visualizer, args = (psong, pcolors))
    t2 = threading.Thread(target=color_cycle)
    t1.start()
    t0.start()
    t2.start()