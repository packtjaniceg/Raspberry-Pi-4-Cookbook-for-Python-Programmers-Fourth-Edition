#!/usr/bin/env python3
''' servo_gui_sw.py

 HARDWARE SETUP
 GPIO
 2[=VX1=2=======]26[=======]40
 1[===0=3=======]25[=======]39
 V=5V X=Gnd
 Servo 0=Base 1=Shoulder 2=Elbow 3=Claw
'''
from guizero import App, Slider, Text
from gpiozero import AngularServo

SERVO_MIN = -45  # - degrees
SERVO_MAX = 45   # + degrees
NAMES = ["Base", "Shoulder", "Elbow", "Claw"]
PINS = ["BOARD7", "BOARD8", "BOARD12", "BOARD11"]

SERVO_CTL = []
for i, name in enumerate(NAMES):
    def func(position):
        ''' slider call function '''
        servo_control(position, i)
    SERVO_CTL.append(func)

def servo_control(position, channel):
    ''' control server position '''
    MY_SERVO[channel].angle = int(position)

APP = App(height=90*len(PINS))
MY_SERVO = []
for i, pin in enumerate(PINS):
    text = Text(APP, text=NAMES[i])
    slide = Slider(APP, start=SERVO_MIN, end=SERVO_MAX,
                   height='fill', width='fill',
                   command=SERVO_CTL[i])
    slide.value = ((SERVO_MAX-SERVO_MIN)/2)+SERVO_MIN
    MY_SERVO.append(
        AngularServo(
            pin,
            initial_angle=((SERVO_MAX-SERVO_MIN)/2)+SERVO_MIN,
            min_angle=SERVO_MIN,
            max_angle=SERVO_MAX))

APP.display()
#End
