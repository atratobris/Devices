#!/usr/bin/python
import logging, logging.handlers, traceback, time, os, json, sys, commands, re
from socket import socket, AF_INET, SOCK_STREAM

sys.path.insert(0, '/usr/lib/python2.7/websocket')
import websocket
###################### LIBRARIES ######################
################## COMPILED TOGETHER ##################

DEFAULT_MAC = "1234"

class Config(object):
    user = os.environ.get('USER')
    operating_system = sys.platform
    mac = None
    @classmethod
    def embedded(cls):
        return cls.user == "root"
    @classmethod
    def getOs(cls):
        return cls.operating_system
    @classmethod
    def getMac(cls):
        if cls.mac == None:
            cls.mac = cls.getMacAddress()
        if cls.getOs() == 'darwin':
            return DEFAULT_MAC
        else:
            return cls.mac
    @classmethod
    def getMacAddress(cls):
        wlanInfo = cls.getWlanInfo()
        if wlanInfo == "Error":
            return
        elif wlanInfo:
            regex = ".*HWaddr (.*)"
            lines = wlanInfo.split("\n")
            for line in lines:
                matched = re.match(regex, line)
                if matched:
                    return matched.group(1)
        return ""
    @classmethod
    def getWlanInfo(cls):
        status, output = commands.getstatusoutput("ifconfig")
        if status == 0:
            for connection in output.split("\n\n"):
                if cls.checkIfWlan(connection):
                    return connection
        else:
            return "Error"
    @classmethod
    def checkIfWlan(cls, text):
        regex = "wlan0.*"
        matched = re.match(regex, str(text))
        if matched:
            return True
        return False

class SERIAL:
  class MSG:
    NAME            = chr(29)
    DATA            = chr(30)
    END             = chr(31)

class Logger:
  if Config.embedded():
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

CHANNEL = "SketchChannel"

def button_handler(msg):
    global ws
    print 'Button Handler received %s..' % msg
    ws.send(ws_message(True, CHANNEL))


def greetings(channel_name):
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

if __name__ == '__main__':
  if Config.embedded():
    ws_url = "ws://caplatform.herokuapp.com/cable"
  else:
    ws_url = "ws://localhost:3000/cable"
  ws = websocket.create_connection(ws_url)
  ws.send(greetings(CHANNEL))
  time.sleep(1)

  if Config.embedded():
    console = Console()
    console.onMessage['button_pressed'] = button_handler
    console.run()
  else:
    idx = 0
    while idx < 1:
      button_handler("Blah")
      time.sleep(1)
      idx += 1
