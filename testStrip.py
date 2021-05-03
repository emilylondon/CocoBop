RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

import pigpio
import time 

pi = pigpio.pi()
audio_max = 255

while True:
    for r in range(audio_max):
        pi.set_PWM_dutycycle(RED_PIN, r)
        time.sleep(0.005)
    for b in range(audio_max, 0, -1):
        pi.set_PWM_dutycycle(BLUE_PIN, b)
        time.sleep(0.005)
    for g in range(audio_max):
        pi.set_PWM_dutycycle(GREEN_PIN, g)
        time.sleep(0.005)
    for r in range(audio_max, 0, -1):
        pi.set_PWM_dutycycle(RED_PIN, r)
        time.sleep(0.005)
    for b in range(audio_max):
        pi.set_PWM_dutycycle(BLUE_PIN, b)
        time.sleep(0.005)
    for g in range(audio_max, 0, -1):
        pi.set_PWM_dutycycle(GREEN_PIN, g)
        time.sleep(0.005)
    

    

    
