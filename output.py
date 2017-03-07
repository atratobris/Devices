#!/usr/bin/python
import sys

sys.path.insert(0, '/usr/lib/python2.7/websocket')
import time, json, websocket

sys.path.insert(0, 'setup/')
sys.path.insert(0, 'drivers/')

from board_setup import BoardSetup
from config import Config

if Config.embedded():
  from output_driver import Driver as Driver
else:
  from test_driver import TestOutputDriver as Driver

CHANNEL = "SketchChannel"
driver = Driver()

DEFAULT_MAC = "5678"

if Config.embedded():
    from bridgeclient import BridgeClient as bridgeclient
    b_client = bridgeclient()


def on_sketch_message(ws, message):
  # transform string to json

  # this is an active message from the server
  if "message" in message and "identifier" in message:
    identifier = json.loads(message["identifier"])
    data = message["message"]
    print "{} from {}".format( data["message"], identifier["channel"])
    driver.set(data['message'])
    return

  # get type of message
  if not "type" in message:
    return

  message_type = message["type"]
  # these are all standard messages which are not of any use
  if message_type == "ping":
    return
  elif message_type == "welcome":
    print "Web socket started"
    return
  elif message_type == "confirm_subscription":
    identifier = json.loads(message["identifier"])
    channel = identifier["channel"]
    print "Subscription to channel {} succesful!".format(channel)
    return


def greetings(channel_name):
    print "MAC: %s" % DEFAULT_MAC
    identifier = {
      "channel": channel_name,
      "mac": DEFAULT_MAC
    }
    regards = {
      "command": "subscribe",
      "identifier": json.dumps(identifier)
    }
    return json.dumps(regards)

def greet(ws):
  ws.send(greetings(CHANNEL))


if __name__ == "__main__":
  if Config.embedded():
    ws_url = "ws://captest.ngrok.io/cable"
  else:
    ws_url = "ws://localhost:3000/cable" 
    
  b_setup = BoardSetup(ws_url, DEFAULT_MAC)
  b_setup.set(on_sketch_message=on_sketch_message)   

  b_setup.run_forever()
