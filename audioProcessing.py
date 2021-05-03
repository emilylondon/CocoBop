RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

from scipy.io.wavfile import read
import numpy as np
import time
import threading
import logging
import pigpio
import os

pi = pigpio.pi()

#set up audio processing parameters
samplerate=44100
resolution=20
spwin=samplerate/resolution

#RMS for np array

#Thread for music player
def music_player():
    logging.info("Playing song now")
    os.system("omxplayer " + "newSong.wav")
    logging.info("Song done")

def audio_visualizer(psong):
    logging.info("Visualizing audio")
    time.sleep(1)
    for t in range(len(psong)):
        audio_max=255*(psong[t]/9000)
        if audio_max > 255:
            audio_max=255
        pi.set_PWM_dutycycle(RED_PIN, audio_max)
        time.sleep(0.05)
    logging.info("Song over")

def window_rms(a, window_size=2):
    energy_list = []
    for s in range(0, a.shape[0], window_size):
        e = s + window_size
        #energy = np.sum(np.abs(a[s:e]**2))
        energy = np.sqrt(np.mean(a[s:e]**2))
        energy_list.append(energy)
    return energy_list

file_name = 'newSong.wav'
a = read(file_name)
r = np.array(a[1], dtype=float)
print(r[0])
print(r.shape)

psong=window_rms(r, window_size=int(spwin))
print(len(psong))
print(psong[1000:1050])
#2205 samples per window 

pi.set_PWM_dutycycle(BLUE_PIN, 0)
pi.set_PWM_dutycycle(GREEN_PIN, 0)

#start visualizing!
if __name__ == "__main__":
    t0 = threading.Thread(target=music_player)
    t1 = threading.Thread(target=audio_visualizer, args = (psong,))
    t1.start()
    t0.start()
    