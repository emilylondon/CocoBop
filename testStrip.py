RED_PIN   = 17
GREEN_PIN = 22
BLUE_PIN  = 24

import pigpio
import time 

pi = pigpio.pi()

while True:
    for r in range(255):
        pi.set_PWM_dutycycle(RED_PIN, r)
        time.sleep(0.005)
    for b in range(255, 0, -1):
        pi.set_PWM_dutycycle(BLUE_PIN, b)
        time.sleep(0.005)
    for g in range(255):
        pi.set_PWM_dutycycle(GREEN_PIN, g)
        time.sleep(0.005)
    for r in range(255, 0, -1):
        pi.set_PWM_dutycycle(RED_PIN, r)
        time.sleep(0.005)
    for b in range(255):
        pi.set_PWM_dutycycle(BLUE_PIN, b)
        time.sleep(0.005)
    for g in range(255, 0, -1):
        pi.set_PWM_dutycycle(GREEN_PIN, g)
        time.sleep(0.005)
    

    

    
