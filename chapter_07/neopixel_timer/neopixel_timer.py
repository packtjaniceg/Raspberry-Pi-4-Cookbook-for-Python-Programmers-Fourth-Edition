#!/usr/bin/python3
''' neopixel_timer.py '''
# sudo pip3 install rpi_ws281x adafruit-circuitpython-neopixel

import sys
import time
import neopixel
import board

RED = (20, 0, 0)
GREEN = (0, 20, 0)
BLUE = (0, 0, 20)
PINK = (20, 0, 20)
YELLOW = (20, 20, 0)
OFF = (0, 0, 0)

MIN = 60
HOUR = 60*MIN
DAY = 24*HOUR

DEFAULT = (2*HOUR)+MIN
DEBUG = True

def do_every(period, func, *args):
    ''' call func every period '''
    def g_tick():
        ''' get next tick '''
        the_time = time.time()
        while True:
            the_time += period
            yield max(the_time - time.time(), 0)
    g = g_tick()
    while True:
        time.sleep(next(g))
        func(*args)


def parse_timer_string(timer_str):
    ''' convert string to seconds int '''
    return int(timer_str.replace("s", ""))

class Timer():
    ''' Neopixel timer '''
    def __init__(self, timer_sec, size=8):
        ''' initialize the timer '''
        self.size = size
        self.timer_seconds = timer_sec
        self.pixels = neopixel.NeoPixel(board.D21, self.size,
                                        auto_write=False)
        self.end_count = 10
    def update(self):
        ''' periodically update the status of the timer '''
        self.print_timer()
        self.display_timer()
        self.update_remaining()
    def print_timer(self):
        ''' display the remaining time on the console '''
        if DEBUG: print(f'{self.timer_seconds}')
    def update_remaining(self, dec_time=1):
        ''' reduce the time remaining '''
        if dec_time > self.timer_seconds:
            self.timer_seconds = 0
        else:
            self.timer_seconds = self.timer_seconds - dec_time
            if DEBUG: print("  <", end="")

    def display_timer(self):
        ''' represent the timer using the NeoPixel display '''
        if self.timer_seconds >= ((self.size)*HOUR):
            remain = ((self.timer_seconds%DAY)/DAY)
            self.display_count(int(self.timer_seconds/DAY),
                               remain=remain, color=YELLOW)
        elif self.timer_seconds >= ((self.size)*MIN):
            remain = ((self.timer_seconds%HOUR)/HOUR)
            self.display_count(int(self.timer_seconds/HOUR),
                               remain=remain, color=BLUE)
        elif self.timer_seconds >= (self.size):
            remain = ((self.timer_seconds%MIN)/MIN)
            self.display_count(int(self.timer_seconds/MIN),
                               remain=remain, color=GREEN)
        elif self.timer_seconds > 0:
            self.display_count(self.timer_seconds-1, color=RED)
        else:
            self.finish()
    def display_count(self, count, remain=0.5, color=RED):
        ''' display the timer count '''
        if DEBUG: print(f'{100*remain:.1f}%', end="")
        self.show_time(count, color)
        self.flash(count, color, remain)
    def show_time(self, count, color):
        ''' display the whole timer units '''
        self.pixels.fill(OFF)
        for i in range(count):
            self.pixels[i] = color
        self.pixels.show()
    def flash(self, num=0, color=RED, on_time=0.5, color_off=OFF):
        ''' flash in proportion to time remaining '''
        self.pixels[num] = color
        self.pixels.show()
        time.sleep(on_time)
        self.pixels[num] = color_off
        self.pixels.show()
    def all_on(self, color=RED):
        ''' switch all LEDs on with selected color '''
        self.pixels.fill(color)
        self.pixels.show()
    def all_off(self):
        ''' switch all LEDs off '''
        self.pixels.fill(OFF)
        self.pixels.show()
    def finish(self):
        ''' indicate the timer has finished '''
        self.end_count = self.end_count-1
        if self.end_count%2:
            self.all_on(color=YELLOW)
        else:
            self.all_on(color=RED)
        if self.end_count == 0:
            self.all_off()
            exit()

if __name__ == '__main__':
    if len(sys.argv) > 1:
        print(f"Args: {sys.argv[1]}")
        timer_seconds = parse_timer_string(sys.argv[1])
    else:
        print(f"Usage: sudo python3 neopixel_timer.py {DEFAULT}s")
        timer_seconds = DEFAULT
    my_timer = Timer(timer_seconds, size=24)

    try:
        do_every(1, my_timer.update)

    except KeyboardInterrupt:
        my_timer.all_off()
#End
