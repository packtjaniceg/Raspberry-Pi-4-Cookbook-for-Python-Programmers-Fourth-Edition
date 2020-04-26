#!/usr/bin/python3
'''rgbtest.py'''
from time import sleep
from gpiozero import RGBLED

#HARDWARE SETUP
# 2[=========XRGB]26[=======]40
# 1[=============]25[=======]39
# X=GND R=Red G=Green B=Blue

#LED CONFIG - Set GPIO Ports
myRGB = RGBLED(red="BOARD22", green="BOARD24", blue="BOARD26")

def main():
    for r in range(0, 10):
        for g in range(0, 10):
            for b in range(0, 10):
                myRGB.color = (r/10, g/10, b/10)
                sleep(0.2)

main()
print("END")
#End
