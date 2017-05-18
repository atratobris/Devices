import sys
from driver_interface import DriverInterface
from phue import Bridge


class Driver(DriverInterface):
  def __init__(self):
    self.input = {}
    self.register_input = None
    self.registerPin = 20
    self.pendingPin = 17
    self.b = Bridge('192.168.1.100')
    self.b.connect()
    while True:
        try:
            self.b.get_api()
            break
        except:
            print "Could not get_api"

    print self.b

  def register_pending(self):
    self.set_lights(True)

  def read_register_status(self):
    return True
    button_pressed = self.get(self.registerPin)
    if button_pressed:
      GPIO.output(self.pendingPin, 0)
    return button_pressed

  def set_lights(self, on):
    for l in self.b.lights:
        l.on = on

  def set(self, data):
      self.set_lights( bool(data['13']) )

  def get(self, input_pin=None):
    if not input_pin:
      input_pin = self.buttonPin
    prev_input = self.input.get(input_pin, None)
    self.input[input_pin] = GPIO.input(input_pin)
    if ((not prev_input) and self.input[input_pin]):
      return True
    return False

  def reset(self):
    self.set_lights(False)
