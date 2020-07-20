#!/usr/bin/env python3
''' avoidance.py
 HARDWARE SETUP
 GPIO
 2[==X==R=======]26[=======]40
 1[===L=lr======]25[=======]39
 X=Gnd
 R=R_FWD, L=L_FWD, r=R_BWD, l=L_BWD
'''
from gpiozero import Button
import rover_drive as drive

OP_CMDS = {'f':'bl', 'b':'fr', 'r':'ll', 'l':'rr', '#':'#'}
# PINS = [L_FWD, L_BWD, R_FWD, R_BWD]
PINS = ["BOARD7", "BOARD11", "BOARD12", "BOARD13"]

class Sensor:
    ''' Sensor class '''
    def __init__(self, pins=None):
        ''' Constructor '''
        pins = pins or PINS
        self.touch = []
        for gpio in pins:
            self.touch.append(Button(gpio))

    def check_sensor(self):
        ''' Check sensor state '''
        for item in self.touch:
            if item.is_pressed:
                return True
        return False

def main():
    ''' Main function '''
    my_bot = drive.Control()
    my_sensors = Sensor()
    while True:
        print("Enter CMDs [f,b,r,l,#]:")
        do_command = input()
        for idx, char in enumerate(do_command.lower()):
            print(f"Step {idx+1} of {len(do_command)}:{char}")
            my_bot.cmd(char, step=0.01)#small steps
            hit = my_sensors.check_sensor()
            if hit:
                print("We hit something on move:" +
                      f" {char} Go: {OP_CMDS[char]}")
                for charcmd in OP_CMDS[char]:
                    my_bot.cmd(charcmd, step=0.01)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Finish")
#End
