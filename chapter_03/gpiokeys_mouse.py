#!/usr/bin/python3
'''gpiokeys_mouse.py'''
import time
import uinput
from gpiozero import Button

#HARDWARE SETUP
# 2[==G=====<==V=]26[=======]40
# 1[===2=1>^=====]25[=======]39
B_DOWN  = "BOARD24"  #V
B_LEFT  = "BOARD18"  #<
B_UP    = "BOARD15"  #^
B_RIGHT = "BOARD13"  #>
B_1  = "BOARD11"     #1
B_2  = "BOARD7"      #2

DEBUG = False
BTN = [Button(B_UP), Button(B_DOWN),
       Button(B_LEFT), Button(B_RIGHT),
       Button(B_1), Button(B_2)]
MSG = ["M_UP", "M_DOWN", "M_LEFT", "M_RIGHT", "1", "Enter"]

def main():
    #Setup uinput
    events_mouse = (uinput.REL_Y, uinput.REL_Y, uinput.REL_X,
                    uinput.REL_X, uinput.BTN_LEFT, uinput.BTN_RIGHT)
    events = events_mouse
    mousemove = 1
    device = uinput.Device(events)
    time.sleep(2) # seconds
    print("DPad Ready!")

    btn_state = [False, False, False, False, False, False]
    while True:
        #Catch all the buttons pressed before pressing the related keys
        for idx, btn in enumerate(BTN):
            if btn.is_pressed:
                btn_state[idx] = True
            else:
                btn_state[idx] = False

        #Perform the button presses/releases
        #(but only change state once)
        for idx, val in enumerate(btn_state):
            if MSG[idx] == "M_UP" or MSG[idx] == "M_LEFT":
                state = -mousemove
            else:
                state = mousemove
            if val:
                device.emit(events[idx], state) # Press.
            elif not val:
                device.emit(events[idx], 0) # Release.
        time.sleep(0.01)

try:
    main()
except KeyboardInterrupt:
    print("Done")
#End
