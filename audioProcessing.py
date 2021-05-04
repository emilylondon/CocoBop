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
BLUE = 255 

#Set up LED, initialize to red 
pi = pigpio.pi()
pi.set_PWM_dutycycle(RED_PIN, RED)
pi.set_PWM_dutycycle(BLUE_PIN, BLUE)
pi.set_PWM_dutycycle(GREEN_PIN, GREEN)

#callback for encoder
#function for reading rotary encoder
def rotary_callback(count):
    global RED
    global GREEN
    global BLUE 

    cscaled = count * 15 
    print(cscaled)
    #if cscaled < 0:
    #    cscaled = 1534
    if cscaled < 255:
        GREEN = cscaled
    elif cscaled < 510:
        RED = 255 - (cscaled-255)
    elif cscaled < 765:
        BLUE = cscaled - 510
    elif cscaled < 1020:
        GREEN = 255 - (count-765)
    elif cscaled < 1275:
        RED = cscaled - 1020
    elif cscaled < 1535:
        BLUE = 255 - (cscaled-1275)
    #elif cscaled > 1535:
    #    cscaled = 0
    time.sleep(0.05)



#Divisor 
ROT_MAX=1023

#set up audio processing parameters
samplerate=44100
resolution=20
spwin=samplerate/resolution

#Color picking thread 
def color_picker():
    global RED
    global BLUE 
    global GREEN
    print("Thread working")
    my_rotary = pigpio_encoder.Rotary(clk=CLK, dt=DT, sw=16)
    my_rotary.setup_rotary(rotary_callback=rotary_callback)
    my_rotary.watch()
    

#Thread for music player
def music_player():
    logging.info("Playing song now")
    os.system("omxplayer " + "newSong.wav")
    logging.info("Song done")

#Visualization thread
def audio_visualizer(psong):
    logging.info("Visualizing audio")
    time.sleep(1)
    global RED
    global BLUE 
    global GREEN
  
    for t in range(len(psong)):
        audio_max=255*(psong[t]/9000)
        if audio_max > 255:
            audio_max=255
        pi.set_PWM_dutycycle(RED_PIN, (audio_max+RED)/2)
        pi.set_PWM_dutycycle(GREEN_PIN, (audio_max+GREEN)/2)
        pi.set_PWM_dutycycle(BLUE_PIN, (audio_max+BLUE)/2)
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
    t2 = threading.Thread(target=color_picker)
    t1.start()
    t0.start()
    t2.start()
    
    