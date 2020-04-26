#!/usr/bin/python3
'''btnroll.py'''
from os import system
from random import randint
from signal import pause
from gpiozero import Button

#HARDWARE SETUP
# 2[==X==1=======]26[=======]40
# 1[=============]25[=======]39
#Button Config
myBtn = Button("BOARD12")

def talk():
    ''' Roll the dice '''
    roll = randint(1, 6)
    print(f"Rolled {roll}")
    system(f"say 'You have thrown a {roll}'")

myBtn.when_pressed = talk
print("Press the button to roll")
pause()
#End
