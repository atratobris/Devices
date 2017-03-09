#!/usr/bin/python
import time, json, sys, os

sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')
import websocket
CHANNEL = "SketchChannel"

from setup.board_setup import BoardSetup
from setup.config import Config

if Config.embedded():
  from drivers.input_driver import Driver as Driver
else:
  from drivers.test_driver import TestInputDriver as Driver

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

def on_open_callback(ws, check_socket_running):
  socket_running = check_socket_running()
  while socket_running:
    response = False
    if response:
      driver.reset()
      button_handler(response, ws)
    socket_running = check_socket_running()
  print "Exiting"

if __name__ == '__main__':

  inputFile = open(os.path.join(os.path.dirname(__file__), 'deviceType.txt'))
  boardType = inputFile.readline().strip()

  if Config.embedded():
    ws_url = "ws://caplatform.herokuapp.com/cable"
  else:
    ws_url = "ws://localhost:3000/cable"

  b_setup = BoardSetup(ws_url, Config.getMac(), driver, boardType)
  b_setup.set(on_open_callback=on_open_callback)

  b_setup.run_forever()
