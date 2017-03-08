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
    return True
    response = self.b_client.get("register_confirmed")
    return ( response and response == 'true' )

  def set(self, data):
    if m_data["type"] == "lcd_display":
      self.b_client.put("LCD", data['value'])
    elif m_data["type"] == "led":
      self.b_client.put("D13", str(int(bool(data['value']))))
    else:
      pass


# LED
#     b_client.put("OUTPUT_CHANNEL", str(int(bool(data))))

# LCD
#     b_client.put("OUTPUT_CHANNEL", data['value'])