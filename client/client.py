import os
import json
import time
import commands
from osHelpers import getMacAddress, getIpAddress


ledValue = False
url  = 'http://captest.ngrok.io/api/board.json'
localUrl = "http://192.168.0.128/arduino/digital/13/"

def setPin(ip, pin, value):
    command ="curl " + ip + "/arduino/digital/" + str(pin) + "/" + str(int(value))
    print command
    status, output = commands.getstatusoutput( command )

def blink(ip, mac):
    global ledValue
    time.sleep(1)
    ledValue = not ledValue
    setPin(ip, 13, ledValue)

def communicate(ip, mac):
    # ip = "192.168.0.128"
    global ledValue

    getInputCommand = "curl -s http://afternoon-wave-57551.herokuapp.com/api/board"
    status, output = commands.getstatusoutput(getInputCommand)
    if status != 0 :
        time.sleep(1)
        return
    print output
    # mock data because Catalin is SLEEPING
    # output = '{"ok": false}'

    # get new led value from API
    try:
        data = json.loads(output)
        newLedValue = bool(int(data["led"]))
    except KeyError:
        print "Key not in json"
        return
    except ValueError:
        print "String not json"
        return


    # if new variable different than previous, call server and change it
    if newLedValue != ledValue:
        ledValue = newLedValue
        setPin(ip, 13, ledValue)

    time.sleep(0.5)

if __name__ == "__main__":
    ip = getIpAddress()
    mac = getMacAddress()

    print "IP:", ip
    print "MAC:", mac
    while True:
        blink(ip, mac)
