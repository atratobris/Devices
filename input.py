#!/usr/bin/python
import time, json, sys

sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')
import websocket
CHANNEL = "SketchChannel"

sys.path.insert(0, 'setup/')
sys.path.insert(0, 'drivers/')
from board_setup import BoardSetup
from config import Config

if Config.embedded():
  from input_driver import Driver as Driver
else:
  from test_driver import TestInputDriver as Driver

driver = Driver()



def button_handler(msg, ws=None):
    if not ws:
      return
    print 'Button Handler received %s..' % msg
    ws.send(ws_message(True, CHANNEL))


def greetings(channel_name):
    print "MAC: %s" % Config.getMac()
    identifier = {
      "channel": channel_name,
      "mac": Config.getMac()
    }
    regards = {
      "command": "subscribe",
      "identifier": json.dumps(identifier)
    }
    return json.dumps(regards)

def ws_message(data_input, channel_name):
    identifier = {
      "channel":channel_name,
      "mac": Config.getMac()
    }
    data = {
      "message": data_input,
      "action": "blink"
    }
    message = {
        "command": "message",
        "identifier":json.dumps(identifier),
        "data": json.dumps(data)
    }
    return json.dumps(message)

def greet(ws):
  ws.send(greetings(CHANNEL))

def on_open_callback(ws):
  while True:
    response = driver.get()
    if response:
      driver.reset()
      button_handler(response, ws)


if __name__ == '__main__':

  if Config.embedded():
    ws_url = "ws://captest.ngrok.io/cable"
  else:
    ws_url = "ws://localhost:3000/cable"

  b_setup = BoardSetup(ws_url, Config.getMac(), driver)
  b_setup.set(on_open_callback=on_open_callback)

  b_setup.run_forever()
