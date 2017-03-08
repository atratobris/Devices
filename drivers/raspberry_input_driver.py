import RPi.GPIO as GPIO

import sys

from driver_interface import DriverInterface


class Driver(DriverInterface):
  def __init__(self):
    self.input = None
    self.register_input = None
    self.buttonPin = 18
    self.registerPin = 20
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.buttonPin, GPIO.IN)
    GPIO.setup(self.registerPin, GPIO.IN)

  def register_pending(self):
    pass #Not yet implemented

  def read_register_status(self):
    return self.get() #Not yet implemented

    prev_input = self.input
    self.input = GPIO.input(self.registerPin)
    if ((not prev_input) and self.register_input):
      return True
    return False


  def get(self):
    prev_input = self.input
    self.input = GPIO.input(self.buttonPin)
    if ((not prev_input) and self.input):
      return True
    return False

  def reset(self):
    pass

