import RPi.GPIO as GPIO

import sys

from driver_interface import DriverInterface


class Driver(DriverInterface):
  def __init__(self):
    self.input = {}
    self.register_input = None
    self.buttonPin = 18
    self.registerPin = 20

    self.registerPin = self.buttonPin #modify later to use different button
    self.pendingPin = 17

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(self.buttonPin, GPIO.IN)
    GPIO.setup(self.registerPin, GPIO.IN)
    GPIO.setup(self.pendingPin, GPIO.OUT, initial=0)

  def register_pending(self):
    GPIO.output(self.pendingPin, 1)

  def read_register_status(self):
    button_pressed = self.get(self.registerPin)
    if button_pressed:
      GPIO.output(self.pendingPin, 0)
    return button_pressed


  def get(self, input_pin=None):
    if not input_pin:
      input_pin = self.buttonPin
    prev_input = self.input[input_pin]
    self.input[input_pin] = GPIO.input(self.buttonPin)
    if ((not prev_input) and self.input[input_pin]):
      return True
    return False

  def reset(self):
    pass

