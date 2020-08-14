#!/usr/bin/python3
'''clocktalk.py'''
from os import system
from datetime import datetime
from signal import pause
from gpiozero import Button

#HARDWARE SETUP
# 2[==X==1=======]26[=======]40
# 1[=============]25[=======]39
#Button Config
myBtn = Button("BOARD12")

def talk():
    ''' Tell the time '''
    the_time = datetime.today().strftime("%-I:%-M %p %A %B %d %Y")
    print(the_time)
    system(f"say {the_time}")

myBtn.when_pressed = talk
print("Press the button to tell the time")
pause()
#End
