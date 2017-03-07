#!/usr/bin/python
import sys

sys.path.insert(0, '/usr/lib/python2.7/websocket')
import thread, time, json, websocket
b_client = None

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


def on_message(ws, message):
  global b_client
  # transform string to json

  # this is an active message from the server
  if "message" in message and "identifier" in message:
    identifier = json.loads(message["identifier"])
    data = message["message"]
    print "{} from {}".format( data["message"], identifier["channel"])
    # pin_status = bool(data["message"])
    driver.set(data['message'])
    # if Config.embedded():
    #   m_data = data["message"]
    #   if m_data["type"] == "lcd_display":
    #     setString(b_client, m_data["value"])
    #   else:
    #     setPin(b_client, 13, bool(pin_status))
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
    time.sleep(1)
  thread.start_new_thread(run, ())


if __name__ == "__main__":
  if Config.embedded():
    ws_url = "ws://captest.ngrok.io/cable"
  else:
    ws_url = "ws://localhost:3000/cable" 
    
  b_setup = BoardSetup(ws_url, DEFAULT_MAC)
  b_setup.set(on_open_callback=on_open, on_sketch_message=on_message)   
  # if Config.embedded():
  #   ws = set_web_socket("ws://caplatform.herokuapp.com/cable")
  # else:
  #   ws = set_web_socket("ws://localhost:3000/cable")
  if Config.embedded():
    while True:
      try:
        b_setup.run_forever()
        time.sleep(5)
      except:
        pass
  else:
    idx = 0;
    print "I'm here"
    while idx < 1:
      try:
        b_setup.run_forever()
        time.sleep(1)
      except:
        pass
      idx += 1
