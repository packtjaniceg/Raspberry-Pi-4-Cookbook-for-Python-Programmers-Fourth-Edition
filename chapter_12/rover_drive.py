#!/usr/bin/env python3
'''rover_drive.py

HARDWARE SETUP
 P1
 2[==X====lRr===]26[=======]40
 1[=======L=====]25[=======]39
'''
import time
from gpiozero import Robot

STEP = 0.2
RIGHT = ("BOARD18", "BOARD22") #[R_FWD, R_BWD]
LEFT = ("BOARD15", "BOARD16")  #[L_FWD, L_BWD]
SPEED = 0.8
DEBUG = True

class Control:
    ''' rover control class '''
    def __init__(self, left=LEFT, right=RIGHT):
        ''' Constructor '''
        self.drive = Robot(left=left, right=right)

    def off(self):
        ''' Stop all motors '''
        self.drive.stop()

    def cmd(self, char, step=STEP):
        ''' Perform required command '''
        if char == 'f':
            self.drive.forward(SPEED)
            time.sleep(step)
        elif char == 'b':
            self.drive.backward(SPEED)
            time.sleep(step)
        elif char == 'r':
            self.drive.right(SPEED)
            time.sleep(step)
        elif char == 'l':
            self.drive.left(SPEED)
            time.sleep(step)
        elif char == '#':
            time.sleep(step)

def main():
    ''' Main function '''
    import os
    if "CMD" in os.environ:
        do_command = os.environ["CMD"]
        enter_input = False
        print(f"CMD={do_command}")
    else:
        enter_input = True
    rover_pi = Control()
    if enter_input:
        print("Enter CMDs [f,b,r,l,#]:")
        do_command = input()
    for idx, char in enumerate(do_command.lower()):
        if DEBUG:
            print(f"Step {idx+1} of {len(do_command)}: {char}")
        rover_pi.cmd(char)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Finish")
#End
