#!/usr/bin/python
import logging
import logging.handlers
import traceback
import time
import os
from socket import socket, AF_INET, SOCK_STREAM
import json, sys

sys.path.insert(0, '/usr/lib/python2.7/websocket')
import websocket
###################### LIBRARIES ######################
################## COMPILED TOGETHER ##################

class SERIAL:
  class MSG:
    NAME            = chr(29)
    DATA            = chr(30)
    END             = chr(31)

class Logger:
  if os.environ.get('USER') == 'root':
    file_name = '/root/YunMessenger.log'
  else:
    file_name = './YunMessenger.log'
  logger = logging.getLogger(__name__)
  logger.setLevel(logging.DEBUG)
  handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=524288, backupCount=0)

  formatter = logging.Formatter()
  formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", '%Y-%m-%d %H:%M:%S')

  handler.setFormatter(formatter)

  logger.addHandler(handler)

class Event(dict):
    def __call__(self, uid, *args, **kwargs):
        if uid in self:
            self[uid](*args, **kwargs)

    def __repr__(self):
        return "Event(%s)" % dict.__repr__(self)

class Console(object):
    pass

    def __init__(self):
      self.connected = False
      self.msg_buffer = ""
      self.logger = Logger.logger
      self.logger.info("Logger initiated")
      self.onMessage = Event()

    def read(self):
      if not self.connected: return None
      index_end = -1

      try:
          new_data = self.console.recv(1024)
      except:
          self.logger.error("Console.recv failed, closing connection")
          self.logger.debug("Traceback: {traceback}".format(traceback=traceback.format_exc()))
          self.console.close()
          self.connected = False
          return None
      if new_data:
          self.msg_buffer += new_data
          index_end = self.msg_buffer.find(SERIAL.MSG.END)

      if new_data == '':
          # client closed the connection
          self.logger.info("Socket connection closed")
          self.console.close()
          self.connected = False
          return None
      if index_end > 0:
          index_name = self.msg_buffer.find(SERIAL.MSG.NAME)
          index_msg = self.msg_buffer.find(SERIAL.MSG.DATA)

          publish_route = ""
          msg = ""

          if index_name >= 0 and index_msg > index_name:
              publish_route = self.msg_buffer[(index_name + 1):index_msg]
              msg = self.msg_buffer[(index_msg + 1):index_end]
              try:
                  self.onMessage(publish_route, msg)
              except Exception:
                  self.logger.error("Publishing the following message "\
                              "to subscriber \"{subscriber}\" failed:\n{message}"\
                              .format(subscriber=publish_route, message=msg))
                  self.logger.debug("Traceback: \n{traceback}".format(traceback=traceback.format_exc()))

          self.msg_buffer = ""

    def run(self):
        self.logger.info("Run initiated")
        self.connected = False
        self.console = socket(AF_INET, SOCK_STREAM)
        while 1:
            if self.connected:
                self.read()
            else:
                try:
                    time.sleep(1)
                    self.logger.info("Attempting to connect to localhost:6571")
                    self.console.close()
                    self.console = socket(AF_INET, SOCK_STREAM)
                    self.console.connect(('localhost', 6571))
                    self.logger.info("Connected to localhost:6571")
                    self.connected = True
                except KeyboardInterrupt:
                    self.logger.info("KeyboardInterrupt, exiting")
                    break
                except:
                    self.logger.error("Can't connect to localhost:6571")
                    self.logger.debug(traceback.format_exc())

###################### END LIBRARIES ######################
######################### OUR CODE ########################

url  = 'http://caplatform.herokuapp.com/api/board.json'
console = Console()
ledOn = False

def button_handler(msg):
    global ws
    global ledOn
    print 'Button Handler received %s..' % msg
    if not ledOn:
        os.system("curl -X POST -d mac='B4:21:8A:F8:2E:23' -d button=True " + url)
        ledOn = not ledOn
        button = True
    else:
        os.system("curl -X POST -d mac='B4:21:8A:F8:2E:23' -d button=False " + url)
        ledOn = not ledOn
        button = False
    ws.send(ws_message(button, "SketchChannel"))


def greetings(channel_name):
    identifier = {
        "channel":channel_name
    }
    regards = {
        "command": "subscribe",
        "identifier": json.dumps(identifier)
    }
    return json.dumps(regards)



def ws_message(data_input, channel_name):
    identifier = {
        "channel":channel_name
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

if __name__ == '__main__':
  global ws
  ws = websocket.create_connection("ws://caplatform.herokuapp.com/cable")
  ws.send(greetings("SketchChannel"))
  time.sleep(1)

  console.onMessage['button_pressed'] = button_handler
  console.run()
