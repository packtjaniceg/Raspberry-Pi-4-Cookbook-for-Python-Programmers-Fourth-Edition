#!/usr/bin/python3
'''ledtest.py'''
from time import sleep
from gpiozero import LED

#HARDWARE SETUP
# 2[=========XGYR]26[=======]40
# 1[=============]25[=======]39
# X=GND G=Green Y=Yellow R=Red

#LED CONFIG - Set GPIO Ports
LED_GREEN = LED("BOARD22"); LED_YELLOW = LED("BOARD24"); LED_RED = LED("BOARD26")
LIGHT = [LED_RED, LED_YELLOW, LED_GREEN]

def main():
    for led in LIGHT:
        led.on()
        print("LED ON")
        sleep(5)
        led.off()
        print("LED OFF")

main()
print("END")
#End
