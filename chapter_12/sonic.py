#!/usr/bin/python3
''' sonic.py '''
import time
from gpiozero import DistanceSensor

TRIGGER = "BOARD13"
ECHO = "BOARD11"

def report_too_close():
    ''' Triggered when too close '''
    print("Back off")

def report_ok():
    ''' Triggered when out of range '''
    print("All Clear")

def main():
    ''' Main function '''
    sensor = DistanceSensor(echo=ECHO, trigger=TRIGGER)
    sensor.when_in_range = report_too_close
    sensor.when_out_of_range = report_ok
    while True:
        print(f"Distance: {sensor.distance*10}cm")
        time.sleep(2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Finish")
#End
