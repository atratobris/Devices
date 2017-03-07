#!/usr/bin/python
import RPi.GPIO as GPIO
import time, os, json, sys, commands, re

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


###################### END LIBRARIES ######################
######################### OUR CODE ########################


CHANNEL = "SketchChannel"


def button_handler(msg):
    global ws
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

def run():
    prev_input = 0
    while True:
        #take a reading
        input = GPIO.input(buttonPin)

        #if the last reading was low and this one high, print
        if ((not prev_input) and input):
            button_handler(str(input))
        #update previous input
        prev_input = input
        #slight pause to debounce
        time.sleep(0.05)

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

  print ws_url
  ws = websocket.create_connection(ws_url)
  ws.send(greetings(CHANNEL))
  time.sleep(1)

  buttonPin = 18
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(buttonPin,GPIO.IN)

  if Config.embedded():
    run()
  else:
    idx = 0
    while idx < 1:
      button_handler("Blah")
      time.sleep(1)
      idx += 1