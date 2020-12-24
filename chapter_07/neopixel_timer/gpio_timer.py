#!/usr/bin/python3
''' gpio_timer.py '''
# sudo pip3 install isodate
import logging
import threading
from flask import Flask
from flask_ask import Ask, statement
import isodate
import neopixel_timer as TIMER

app = Flask(__name__)
ask = Ask(app, '/')

logging.basicConfig(filename="gpio_timer.log", level=logging.DEBUG)
logging.debug("Starting gpio_timer")

class TheTimer:
    ''' Class to control the timer '''
    def __init__(self):
        ''' Initialise the timer '''
        self._running = True

    def terminate(self):
        ''' Stop the timer '''
        self._running = False

    def run(self, timer_seconds):
        ''' Start the timer for the required time '''
        try:
            my_timer = TIMER.Timer(timer_seconds, size=24)
            TIMER.do_every(1, my_timer.update)
            print("Complete")
        except Exception as e:
            print(e)

@ask.intent('StartPiTimerIntent', mapping={'period': 'period'})
def start_my_timer(period):
    ''' Handle the intent to start the timer '''
    print("kick off timer here")
    print(period)
    try:
        duration = isodate.parse_duration(period)
        print(duration)
        timer_seconds = int(duration.total_seconds())
        print(timer_seconds)
        timer = TheTimer()
        thread = threading.Thread(target=timer.run, args=(timer_seconds, ))
        thread.start()

    except Exception as e:
        print(e)
        return statement('It did not work {}'.format(duration))
    return statement('Starting timer for {}'.format(period))

if __name__ == '__main__':
    try:
        app.run(debug=True)
    except Exception as e:
        print(e)
#End
