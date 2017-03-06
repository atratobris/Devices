#!/usr/bin/python
import time, os, json, sys, commands, re

sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')
import websocket
from socket import gaierror
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
            cls.mac = cls.getMacAddress().strip()
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

if Config.embedded():
    from bridgeclient import BridgeClient as bridgeclient
    b_client = bridgeclient()


###################### END LIBRARIES ######################
######################### OUR CODE ########################


CHANNEL = "SketchChannel"

if Config.embedded():
  url = "caplatform.herokuapp.com"
else:
  url = "localhost:3000"
ws = None

def button_handler(msg):
    global ws
    print 'Button Handler received %s..' % msg
    ws.send(ws_message(True, CHANNEL))


def greetings(channel_name):
  print "Registering device %s for SketchChannel" % Config.getMac()
  identifier = {
    "channel": channel_name,
    "mac": Config.getMac()
  }
  regards = {
    "command": "subscribe",
    "identifier": json.dumps(identifier)
  }
  return json.dumps(regards)

def run():
  while True:
    response = b_client.get("BP")
    if (response and response == 'true'):
      b_client.put("BP", "false")
      button_handler(response)

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

def setup_connection(url):
  global ws
  timeout = 1
  retry_count = 10
  for i in xrange(retry_count):
    try:
      ws = websocket.create_connection("ws://%s/cable" % url)
    except gaierror as e:
      print "Input for %s failed %s. Retry: %d timeout: %d" % (Config.getMac(), str(e), i, timeout)
      if i < retry_count:
        time.sleep(timeout)
        timeout *= 2
      else:
        raise e

if __name__ == '__main__':
  print url
  setup_connection(url)
  ws.send(greetings(CHANNEL))
  time.sleep(1)

  if Config.embedded():
    run()
  else:
    idx = 0
    while idx < 1:
      button_handler("true")
      time.sleep(1)
      idx += 1
