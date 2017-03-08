import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')

from driver_interface import DriverInterface
from bridgeclient import BridgeClient as bridgeclient


class Driver(DriverInterface):
  def __init__(self):
    self.b_client = bridgeclient()

  def register_pending(self):
    self.b_client.put("pending", "true")

  def read_register_status(self):
    response = self.b_client.get("BP")
    return ( response and response == 'true' )

  def get(self):
    response = self.b_client.get("BP")
    return (response and response == 'true')

  def reset(self):
    self.b_client.put("BP", "false")

