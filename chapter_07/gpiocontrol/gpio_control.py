#!/usr/bin/env python3
from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import logging

GPIO.setmode(GPIO.BOARD)
app = Flask(__name__)
ask = Ask(app, '/')

logging.basicConfig(filename="gpio_control.log", level=logging.DEBUG)
logging.debug("Starting gpio_control")

@ask.intent('GPIOControlIntent', mapping={'status': 'status', 'pin': 'pin'})
def gpio_control(status, pin):
  try:
    pinNum = int(pin)
  except Exception as e:
    return statement('Pin number not valid.')
  GPIO.setup(pinNum, GPIO.OUT)
  if status in ['on', 'high']:
    GPIO.output(pinNum, GPIO.HIGH)
    logging.debug('Turning pin {} {}'.format(pinNum, "HIGH"))
  if status in ['off', 'low']:
    GPIO.output(pinNum, GPIO.LOW)
    logging.debug('Turning pin {} {}'.format(pinNum, "LOW"))
  logging.debug('Turning pin {} {}'.format(pin, status))
  return statement('Turning pin {} {}'.format(pin, status))

if __name__ == '__main__':
  app.run(debug=True)
