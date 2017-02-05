import os
import json
import time
from osHelpers import getMacAddress, getIpAddress


ledValue = True
url  = 'http://captest.ngrok.io/api/board.json'
localUrl = "http://192.168.0.128/arduino/digital/13/"

def setPin(ip, pin, value):
    command ="curl " + ip + "/arduino/digital/" + str(pin) + "/" + str(int(value))
    print command
    os.system( command)

def blink(ip, mac):
    global ledValue
    time.sleep(1)
    ledValue = not ledValue
    setPin(ip, 13, ledValue)

def communicate():
    global ledValue
    global url

    time.sleep(3)
    ledValue = not ledValue



    body = os.system("curl " + url)
    # print body
    # resp = json.loads(body)
    # print resp

    # print error

    # if r["ok"] == False:
    #     continue

    # print r
    # print "posting..."
    # p = requests.post('http://captest.ngrok.io/api/board', data = {'led':True})

    os.system("curl -X POST -d mac='B4:21:8A:F5:0E:A4' -d button="+str(ledValue) + " " + url)




if __name__ == "__main__":
    ip = getIpAddress()
    mac = getMacAddress()

    print "IP:", ip
    print "MAC:", mac
    while True:
        blink(ip, mac)

# curl -X PUT -d status="$status" -d result="$(tail -n 100 result.out)" $URL
