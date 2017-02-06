import os
import re
import json
import time
import commands

ledValue = True
url  = 'http://captest.ngrok.io/api/board.json'
localUrl = "http://192.168.0.128/arduino/digital/13/"
reg = ".*.*"

def getConnections(text):
    connections = text.split("\n\n")
    return connections

def checkIfWlan(text):
    regex = "wlan0.*"
    matched = re.match(regex, str(text))
    if matched :
        return True
    return False

def getMacAddress():
    wlanInfo = getWlanInfo()
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

def getWlanInfo():
    status, output = commands.getstatusoutput("ifconfig")
    if status == 0:
        connections = getConnections(output)

        for connection in connections:
            if checkIfWlan(connection):
                return connection
    else:
        print "command results in error"
        return "Error"

def getIpAddress():
    wlanInfo = getWlanInfo()
    if wlanInfo == "Error":
        return
    elif wlanInfo:
        regex = ".*inet addr:(.*)  Bcast.*"
        lines = wlanInfo.split("\n")
        for line in lines:
            matched = re.match(regex, line)
            if matched:
                return matched.group(1)
    return ""

def setPin(ip, pin, value):
  command = "curl http://root:doghunter@" + ip + "/arduino/digital/" + str(pin) + "/" + str(int(value))
  print command
  os.system( command)

def blink(ip, mac):
  global ledValue
  time.sleep(1)
  ledValue = not ledValue
  setPin(ip, 13, ledValue)

def communicate(ip):
  _, response =  commands.getstatusoutput("curl -s " + url)
  pin_status = json.loads(response)["led"]
  print "Setting the pin to %s..\n" % pin_status
  setPin(ip, 13, pin_status)

if __name__ == "__main__":
  ip = getIpAddress()
  mac = getMacAddress()

  print "IP:", ip
  print "MAC:", mac
  while True:
      communicate(ip)
