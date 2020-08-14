#!/usr/bin/python3
'''gpiokeys.py'''
import time
from gpiozero import Button
import uinput

#HARDWARE SETUP
# 2[==G=====<==V=]26[=======]40
# 1[===2=1>^=====]25[=======]39
B_DOWN  = "BOARD24"  #V
B_LEFT  = "BOARD18"  #<
B_UP    = "BOARD15"  #^
B_RIGHT = "BOARD13"  #>
B_1  = "BOARD11"     #1
B_2  = "BOARD7"      #2

DEBUG = True
BTN = [Button(B_UP), Button(B_DOWN),
       Button(B_LEFT), Button(B_RIGHT),
       Button(B_1), Button(B_2)]
MSG = ["UP", "DOWN", "LEFT", "RIGHT", "1", "2"]

def main():
    #Setup uinput
    events = (uinput.KEY_UP, uinput.KEY_DOWN, uinput.KEY_LEFT,
              uinput.KEY_RIGHT, uinput.KEY_ENTER, uinput.KEY_ENTER)
    device = uinput.Device(events)
    time.sleep(2) # seconds
    print("DPad Ready!")

    btn_state = [False, False, False, False, False, False]
    key_state = [False, False, False, False, False, False]
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
            if val and not key_state[idx]:
                if DEBUG: print(str(val) + ":" + MSG[idx])
                device.emit(events[idx], 1) # Press.
                key_state[idx] = True
            elif not val and key_state[idx]:
                if DEBUG: print(str(val) + ":!" + MSG[idx])
                device.emit(events[idx], 0) # Release.
                key_state[idx] = False
        time.sleep(0.1)

try:
    main()
except KeyboardInterrupt:
    print("Done")
#End
