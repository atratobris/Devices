import RPi.GPIO as GPIO

import sys

from driver_interface import DriverInterface


class Driver(DriverInterface):
  def __init__(self):
    self.input = {}
    self.register_input = None
    self.ledPin = 18
    self.registerPin = 20

    self.registerPin = self.ledPin #modify later to use different button
    self.pendingPin = 17

    GPIO.setmode(GPIO.BCM)

    GPIO.setup(self.ledPin, GPIO.OUT)
    GPIO.setup(self.registerPin, GPIO.IN)
    GPIO.setup(self.pendingPin, GPIO.OUT, initial=0)

  def register_pending(self):
    GPIO.output(self.pendingPin, 1)

  def read_register_status(self):
    return True
    button_pressed = self.get(self.registerPin)
    if button_pressed:
      GPIO.output(self.pendingPin, 0)
    return button_pressed

  def set(self, data):
    if data["type"] == "lcd_display":
      pass
    elif data["type"] == "led":
      GPIO.output(self.ledPin, int(bool(data['13'])))
    else:
      pass

  def get(self, input_pin=None):
    if not input_pin:
      input_pin = self.buttonPin
    prev_input = self.input.get(input_pin, None)
    self.input[input_pin] = GPIO.input(input_pin)
    if ((not prev_input) and self.input[input_pin]):
      return True
    return False

  def reset(self):
    pass

