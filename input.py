#!/usr/bin/python
import time, json, sys, thread

sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')
import websocket
from board_setup import BoardSetup
from config import Config

if Config.embedded():
  from input_driver import Driver as Driver
else:
  from test_driver import TestInputDriver as Driver


CHANNEL = "SketchChannel"
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

def on_open(ws, is_registered, is_pending, register_callback):
  def run(*args):
    while not is_registered():
      if is_pending():
        print 'Pending'
        driver.register_pending()
        registered_pressed = driver.read_register_status()
        if registered_pressed:
          register_callback()
      else:
        print 'Unregistered'
        time.sleep(2)
    print 'Registered'
    greet(ws)
    while True:
      response = driver.get()
      if response:
        driver.reset()
        button_handler(response, ws)
      time.sleep(60)
  thread.start_new_thread(run, ())


if __name__ == '__main__':

  if Config.embedded():
    ws_url = "ws://captest.ngrok.io/cable"
  else:
    ws_url = "ws://localhost:3000/cable"

  b_setup = BoardSetup(ws_url, Config.getMac())
  b_setup.set(on_open_callback=on_open)

  if Config.embedded():
    while True:
      try:
        b_setup.run_forever()
        time.sleep(5)
      except:
        pass
  else:
    idx = 0;
    # Don't try to restart server
    while idx < 1:
      try:
        b_setup.run_forever()
        time.sleep(1)
      except:
        pass
      idx += 1

