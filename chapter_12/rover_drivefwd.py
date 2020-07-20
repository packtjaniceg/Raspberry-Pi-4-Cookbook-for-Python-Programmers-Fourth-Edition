#!/usr/bin/env python3
''' rover_drivefwd.py

HARDWARE SETUP
 P1
 2[==X====LR====]26[=======]40
 1[=============]25[=======]39
'''
import time
from gpiozero import DigitalOutputDevice

ON = 1
OFF = 0
STEP = 0.5
PINS = ["BOARD16", "BOARD18"] # PINS=[L-motor, R-motor]
FWD = [ON, ON]
RIGHT = [ON, OFF]
LEFT = [OFF, ON]
DEBUG = True

class Control:
    ''' rover control class '''
    def __init__(self, pins=None):
        ''' Constructor '''
        self.pins = pins or PINS
        self.motors = []
        for gpio in self.pins:
            self.motors.append(DigitalOutputDevice(pin=gpio))

    def off(self):
        ''' Stop all motors '''
        for motor in self.motors:
            motor.value = OFF

    def drive(self, drive, step=STEP):
        ''' Move in required direction '''
        for idx, motor in enumerate(self.motors):
            motor.value = drive[idx]
            if DEBUG:
                print(f"{self.pins[idx]}:{drive[idx]}")
        time.sleep(step)
        self.off()

    def cmd(self, char, step=STEP):
        ''' Perform required command '''
        if char == 'f':
            self.drive(FWD, step)
        elif char == 'r':
            self.drive(RIGHT, step)
        elif char == 'l':
            self.drive(LEFT, step)
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
        print("Enter CMDs [f,r,l,#]:")
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
