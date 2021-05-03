from scipy.io.wavfile import read
import numpy as np
import time
import threading
import logging
import pigpio
import os
import sys

sys.path.append('/venv/Dexter/GrovePi/Software/Python') #grovepi stuff

import grovepi

#set up input pins for rotary encoder and LED pins
RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24
PORT_ROTARY = 1

#Set up LED, initialize to red 
pi = pigpio.pi()
pi.set_PWM_dutycycle(RED_PIN, 255)
pi.set_PWM_dutycycle(BLUE_PIN, 0)
pi.set_PWM_dutycycle(GREEN_PIN, 0)

#Brightness Values for RGB, make them global so they can be modified across threads
global RED 
RED = 255
global GREEN
GREEN = 0
global BLUE 
BLUE = 0

#Divisor 
ROT_MAX=1023

#set up audio processing parameters
samplerate=44100
resolution=20
spwin=samplerate/resolution

#set up GrovePi pin
grovepi.pinMode(PORT_ROTARY, "INPUT")

#Thread for color picking 
def c_pick():
    while True:
        rdg = grovepi.analogRead(PORT_ROTARY)
    if rdg < 170:
        GREEN = 1.5*rdg
    elif rdg < 340:
        RED = 255-(1.5*(rdg-170))
    elif rdg < 510:
        BLUE = 1.5 * (rdg-340)
    elif rdg < 680:
        GREEN = 255 - (1.5*(rdg-510))
    elif rdg < 850:
        RED = 1.5 * (rdg-680)
    elif rdg < 1020:
        BLUE = 255 - (1.5*(rdg-850))

#Thread for music player
def music_player():
    logging.info("Playing song now")
    os.system("omxplayer " + "newSong.wav")
    logging.info("Song done")

#Visualization thread
def audio_visualizer(psong):
    logging.info("Visualizing audio")
    time.sleep(1)
    for t in range(len(psong)):
        audio_max=255*(psong[t]/9000)
        if audio_max > 255:
            audio_max=255
        pi.set_PWM_dutycycle(RED_PIN, audio_max*RED)
        pi.set_PWM_dutycycle(GREEN_PIN, audio_max*GREEN)
        pi.set_PWM_dutycycle(BLUE_PIN, audio_max*BLUE)
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
    t2 = threading.Thread(target=c_pick)
    t1.start()
    t0.start()
    t2.start()
    