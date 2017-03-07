import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')

from driver_interface import DriverInterface
from bridgeclient import BridgeClient as bridgeclient


class Driver(DriverInterface):
  def __init__(self):
    b_client = bridgeclient()

  def register_pending(self):
    b_client.put("pending", "true")

  def read_register_status(self):
    response = b_client.get("register_confirmed")
    return ( response and response == 'true' )

  def set(self, data):
    b_client.put("OUTPUT_CHANNEL", str(int(data)))


# LED
#     b_client.put("OUTPUT_CHANNEL", str(int(bool(data))))

# LCD
#     b_client.put("OUTPUT_CHANNEL", data['value'])