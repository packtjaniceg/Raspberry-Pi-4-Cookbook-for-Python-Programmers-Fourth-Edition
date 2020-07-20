#!/usr/bin/env python3
'''bug_drive.py'''
import time
import servo_control_hw as servoCon

SERVOMIN = 205  # Min pulse 1000us 204.8 (50Hz)
SERVOMAX = 410  # Max pulse 2000us 409.6 (50Hz)

SERVO_L = 0; SEFVO_M = 1; SERVO_R = 2
TILT = 20
MOVE = 30
MID = ((SERVOMAX-SERVOMIN)/2)+SERVOMIN
CW = MID+MOVE; ACW = MID-MOVE
TR = MID+TILT; TL = MID-TILT
FWD = [TL, ACW, ACW, TR, CW, CW] #[midL,fwd,fwd,midR,bwd,bwd]
BWD = [TR, ACW, ACW, TL, CW, CW] #[midR,fwd,fwd,midL,bwd,bwd]
LEFT = [TR, ACW, CW, TL, CW, ACW] #[midR,fwd,bwd,midL,bwd,fwd]
RIGHT = [TL, ACW, CW, TR, CW, ACW] #[midL,fwd,bwd,midR,bwd,fwd]
HOME = [MID, MID, MID, MID, MID, MID]
PINS = [SEFVO_M, SERVO_L, SERVO_R, SEFVO_M, SERVO_L, SERVO_R]
STEP = 0.2
SPEED = 0.1
DEBUG = False

class Control:
    ''' bug control class '''
    def __init__(self, pins=None, steptime=STEP):
        ''' Constructor '''
        self.pins = pins or PINS
        self.steptime = steptime
        self.the_servo = servoCon.Servo()

    def off(self):
        ''' Reset to Home position '''
        self.drive(HOME, STEP)

    def drive(self, drive, step=STEP):
        ''' Move in required direction '''
        for idx, servo in enumerate(self.pins):
            if drive[idx] == SEFVO_M:
                time.sleep(step)
            self.the_servo.set_pwm(servo, 0, drive[idx])
            if drive[idx] == SEFVO_M:
                time.sleep(step)
            if DEBUG:
                print(f"{servo}:{drive[idx]}")
            time.sleep(SPEED)

    def cmd(self, char, step=STEP):
        ''' Perform required command '''
        if char == 'f':
            self.drive(FWD, step)
        elif char == 'b':
            self.drive(BWD, step)
        elif char == 'r':
            self.drive(RIGHT, step)
        elif char == 'l':
            self.drive(LEFT, step)
        elif char == 'h':
            self.drive(HOME, step)
        elif char == '#':
            time.sleep(step)

def main():
    ''' Main function '''
    import os
    if "CMD" in os.environ:
        do_command = os.environ["CMD"]
        enter_input = False
        print("CMD="+do_command)
    else:
        enter_input = True
    bug_pi = Control()
    if enter_input:
        print("Enter CMDs [f,b,r,l,h,#]:")
        do_command = input()
    for idx, char in enumerate(do_command.lower()):
        if DEBUG:
            print(f"Step {idx+1} of {len(do_command)}: char")
        bug_pi.cmd(char)

if __name__ == '__main__':
    try:
        DEBUG = True
        main()
    except KeyboardInterrupt:
        print("Finish")
#End
