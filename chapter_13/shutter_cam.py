#!/usr/bin/python3
''' shutter_cam.py '''
import time
import RPi.GPIO as GPIO
import cam.CameraGUI as camGUI


GPIO.setmode(GPIO.BOARD)
CAMERA_BTN = 12 #GPIO Pin 12
GPIO.setup(CAMERA_BTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
count = 1
try:
    while True:
        btn_val = GPIO.input(CAMERA_BTN)
        #Take photo when Pin 12 at 0V
        if not btn_val:
            camGUI.CameraGUI.cam_capture("Snap%03d.jpg"%count,
                                         camGUI.SET.NORM_SIZE)
            count += 1
        time.sleep(0.1)
finally:
    GPIO.cleanup()
#End
