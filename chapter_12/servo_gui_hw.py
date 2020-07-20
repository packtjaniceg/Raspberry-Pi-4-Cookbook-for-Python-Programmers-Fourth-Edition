#!/usr/bin/env python3
''' servo_gui_hw.py

 HARDWARE SETUP
 GPIO
 2[==X==========]26[=======]40
 1[VDC==========]25[=======]39
 V=3.3V X=Gnd
 D=SDA C=SCL
'''
from guizero import App, Slider, Text
import servo_control_hw as servoCon

SERVO_MIN = 205  # Min pulse 1ms 204.8 (50Hz)
SERVO_MAX = 410  # Max pulse 2ms 409.6 (50Hz)
NAMES = ["SERVO_L", "SEFVO_M", "SERVO_R"]

SERVO_CTL = []
for i, name in enumerate(NAMES):
    def func(position):
        ''' slider call function '''
        servo_control(position, i)
    SERVO_CTL.append(func)

def servo_control(position, channel):
    ''' control server position '''
    MY_SERVO.set_pwm(channel, 0, position)

APP = App(height=90*len(NAMES))
MY_SERVO = servoCon.Servo()
for i, name in enumerate(NAMES):
    text = Text(APP, text=name)
    slide = Slider(APP, start=SERVO_MIN, end=SERVO_MAX,
                   height='fill', width='fill',
                   command=SERVO_CTL[i])
    slide.value = ((SERVO_MAX-SERVO_MIN)/2)+SERVO_MIN

APP.display()
#End
