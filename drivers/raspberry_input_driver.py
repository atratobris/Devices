import RPi.GPIO as GPIO

import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')

from driver_interface import DriverInterface
from bridgeclient import BridgeClient as bridgeclient


class Driver(DriverInterface):
  def __init__(self):
    self.input = None
    self.buttonPin = 18
    GPIO.setMode(GPIO.BCM)
    GPIO.setup(self.buttonPin, GPIO.IN)

  def register_pending(self):
    b_client.put("pending", "true")

  def read_register_status(self):
    response = b_client.get("register_confirmed")
    return ( response and response == 'true' )

  def get(self):
    prev_input = self.input
    self.input = GPIO.input(self.buttonPin)
    if ((not prev_input) and self.input):
      return True

  def reset(self):
    pass

