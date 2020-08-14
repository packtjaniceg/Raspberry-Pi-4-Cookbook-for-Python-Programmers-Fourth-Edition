#!/usr/bin/python3
'''toggletest.py'''
from time import sleep
from gpiozero import Button

#HARDWARE SETUP
# 2[==X==1=======]26[=======]40
# 1[=============]25[=======]39
#Button Config
myBtn = Button("BOARD12")
print("Press button")

state = False
btnClosed = False
while True:
    if myBtn.is_pressed and not btnClosed:
        btnClosed = True
        state = not state
        print(f"State:{state}")
    elif not myBtn.is_pressed and btnClosed:
        btnClosed = False
    sleep(0.1)

#End
