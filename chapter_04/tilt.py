#!/usr/bin/python3
'''tilt.py'''
import RPi.GPIO as GPIO
#HARDWARE SETUP
# 2[===========T=]26[=======]40
# 1[=============]25[=======]39
#Tilt Config
TILT_SW = 24

def tilt_setup():
    #Setup the wiring
    GPIO.setmode(GPIO.BOARD)
    #Setup Ports
    GPIO.setup(TILT_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def tilt_moving():
    #Report the state of the Tilt Switch
    return GPIO.input(TILT_SW)

def main():
    import time
    tilt_setup()
    while True:
        print("TILT %s"% (GPIO.input(TILT_SW)))
        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
        print("Closed Everything. END")
#End
