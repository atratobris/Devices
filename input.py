#!/usr/bin/python
import time, os, json, sys, commands, re

sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')
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

if Config.embedded():
    from bridgeclient import BridgeClient as bridgeclient
    b_client = bridgeclient()


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

if __name__ == '__main__':
  if Config.embedded():
    ws_url = "ws://caplatform.herokuapp.com/cable"
  else:
    ws_url = "ws://localhost:3000/cable"
  ws = websocket.create_connection(ws_url)
  ws.send(greetings(CHANNEL))
  time.sleep(1)

  if Config.embedded():
    run()
  else:
    idx = 0
    while idx < 1:
      button_handler("Blah")
      time.sleep(1)
      idx += 1
