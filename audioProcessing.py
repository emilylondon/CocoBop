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

RED=0
GREEN = 0
BLUE = 0 
flag = 0

#Set up LED, initialize to red 

pi = pigpio.pi()
pi.set_PWM_dutycycle(RED_PIN, RED)
pi.set_PWM_dutycycle(BLUE_PIN, BLUE)
pi.set_PWM_dutycycle(GREEN_PIN, GREEN)

#helper function for LED outputs 

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
        RED = 0
        GREEN = 0
        BLUE = 255
        while flag == 0: 
            for r in range(255):
                RED = r
                time.sleep(0.05)
            for b in range(255, 0, -1):
                BLUE = b
                time.sleep(0.05)
            for g in range(255):
                GREEN = g
                time.sleep(0.05)
            for r in range(255, 0, -1):
                RED = r 
                time.sleep(0.05)
            for b in range(255):
                BLUE = b
                time.sleep(0.05)
            for g in range(255, 0, -1):
                GREEN = g
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
def audio_visualizer(psong):
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
        time.sleep(0.05)
    logging.info("Song over")

#function for RMS 
def window_rms(a, window_size=2):
    energy_list = []
    for s in range(0, a.shape[0], window_size):
        e = s + window_size
        #energy = np.sum(np.abs(a[s:e]**2))
        energy = np.sqrt(np.mean(a[s:e]**2))
        energy_list.append(energy)
    return energy_list
#read in file
file_name = 'newSong.wav'
print("File downloaded and loaded in")
a = read(file_name)
r = np.array(a[1], dtype=float)
print(r[0])
print(r.shape)
#2205 samples per window 
psong=window_rms(r, window_size=int(spwin))
#start visualizing!
if __name__ == "__main__":
    t0 = threading.Thread(target=music_player)
    t1 = threading.Thread(target=audio_visualizer, args = (psong,))
    t2 = threading.Thread(target=color_cycle)
    t1.start()
    t0.start()
    t2.start()