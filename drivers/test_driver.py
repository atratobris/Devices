from driver_interface import DriverInterface

import time, sys

class TestInputDriver(DriverInterface):
  def __init__(self):
    self.pending_for = 0

  def register_pending(self):
    self.pending_for += 1
    time.sleep(2)

  def read_register_status(self):
    if self.pending_for == 3:
      self.pending_for = 0
      return True
    return False

  def get(self):
    # print "Sim the press of a button: "
    # msg = sys.stdin.readline()
    msg = raw_input("Sim the press of a button: ")
    return True


  def reset(self):
    pass

class TestOutputDriver(DriverInterface):
  def __init__(self):
    self.pending_for = 0

  def register_pending(self):
    self.pending_for += 1
    time.sleep(2)

  def read_register_status(self):
    if self.pending_for == 3:
      self.pending_for = 0
      return True
    return False

  def set(self, data):
    print data

