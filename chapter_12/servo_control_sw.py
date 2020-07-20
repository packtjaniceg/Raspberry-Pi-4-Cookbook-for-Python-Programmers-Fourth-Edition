#!/usr/bin/env python3
''' servo_control_sw.py

 HARDWARE SETUP
 GPIO
 2[=VX1=2=======]26[=======]40
 1[===0=3=======]25[=======]39
 V=5V X=Gnd
 Servo 0=Base 1=Shoulder 2=Elbow 3=Claw
'''
import curses
from gpiozero import AngularServo

CAL = [90, 90, 90, 90]
MIN = [0, 60, 40, 60]; MAX = [180, 165, 180, 180]
PINS = ["BOARD7", "BOARD8", "BOARD12", "BOARD11"]
POS = list(CAL)
KEY_CMD = [ord('r'), ord('x')]
#Keys to rotate counter-clockwise
KEY_LESS = {ord('d'):0, ord('s'):1, ord('j'):2, ord('k'):3}
#Keys to rotate clockwise
KEY_MORE = {ord('a'):0, ord('w'):1, ord('l'):2, ord('i'):3}

STEP = 5; LESS = -STEP; MORE = STEP #Define control steps
DEBUG = True

def setup(pins=None):
    ''' setup servos '''
    gpio = pins or PINS
    servos = []
    for i, val in enumerate(gpio):
        servos.append(AngularServo(val,
                                   initial_angle=CAL[i],
                                   min_angle=MIN[i],
                                   max_angle=MAX[i]))
    return servos

def limit_servo(servo, value):
    ''' keep servos within range limits '''
    lim_value = value
    if value > MAX[servo]:
        lim_value = MAX[servo]
    elif value < MIN[servo]:
        lim_value = MIN[servo]
    return lim_value

def update_servo(servo, change):
    ''' change the position of the servo '''
    POS[servo] = limit_servo(servo, POS[servo]+change)
    set_servo(servo, POS[servo])
    return str(POS)

def set_servo(servo, position):
    ''' set the position of the servo '''
    SERVOS[servo].angle = position

def calibrate():
    ''' return servos to their calibration positions '''
    for i, value in enumerate(CAL):
        POS[i] = value
        set_servo(i, value)

def main(term):
    ''' provide keyboard control '''
    text = "Me Arm Control:\n" + \
           " Turn: a-d\n" + \
           " Shoulder: w-s\n" + \
           " Elbow: j-l\n" + \
           " Claw: i-k\n" + \
           " Reset-Cal: r \n" + \
           " eXit: x\n"
    term.nodelay(1)
    term.move(1, 0)
    term.addstr(text)
    term.refresh()
    while True:
        term.move(10, 0)
        char = term.getch()
        if char != -1:
            if char in KEY_MORE:
                text = update_servo(KEY_MORE[char], MORE)
            elif char in KEY_LESS:
                text = update_servo(KEY_LESS[char], LESS)
            elif char in KEY_CMD:
                if char == ord('r'):
                    calibrate()
                    text = "Reset-Calibration"
                elif char == ord('x'):
                    exit()
            if DEBUG:
                term.addstr(text+"   ")

SERVOS = setup()

if __name__ == '__main__':
    curses.wrapper(main)
#End
