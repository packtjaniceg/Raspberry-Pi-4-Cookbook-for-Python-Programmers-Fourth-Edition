#!/usr/bin/env python3
''' compassDrive.py '''
import time
import xlo_borg3 as XLoBorg
import rover_drive as drive

MARGIN = 10 #turn until within 10degs
LEFT = "l"; RIGHT = "r"; DONE = "#"

def cal_dir(target, current, margin=MARGIN):
    ''' Calculate direction to reach angle '''
    target = target%360
    current = current%360
    delta = (target-current)%360
    print(f"Target={target:.2f} Current={current:.2f} Delta={delta:.2f}")
    if delta <= margin:
        command = DONE
    else:
        if delta > 180:
            command = LEFT
        else:
            command = RIGHT
    return command

def main():
    ''' Control direction of robot based on target angle '''
    my_compass = XLoBorg.Compass()
    my_bot = drive.Control()
    while True:
        print("Enter target angle:")
        angle_target = input()
        try:
            command = LEFT
            while command != DONE:
                angle_compass = my_compass.read_compass_angle()
                command = cal_dir(float(angle_target), angle_compass)
                print(f"CMD: {command}")
                time.sleep(1)
                my_bot.cmd(command)
            print("Angle Reached!")
        except ValueError:
            print("Enter valid angle!")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Finish")
#End
