import os
import json
import time
import commands
from osHelpers import getMacAddress, getIpAddress


ledValue = True
url  = 'http://captest.ngrok.io/api/board.json'
localUrl = "http://192.168.0.128/arduino/digital/13/"

def setPin(ip, pin, value):
  command ="curl http://root:doghunter@" + ip + "/arduino/digital/" + str(pin) + "/" + str(int(value))
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
