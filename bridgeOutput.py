#!/usr/bin/python

import commands, json, sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')

from time import sleep
from bridgeclient import BridgeClient as bridgeclient

url  = 'http://caplatform.herokuapp.com/api/board'

# cl: bridgeclient instance
def blink(cl):
    cl.put('D12','0')
    cl.put('D13','1')
    sleep(0.1)
    cl.put('D12','1')
    cl.put('D13','0')
    sleep(0.1)

# value: 0 or 1
# pin: integer
# cl: bridgeclient instance
def setPin(cl, pin, value):
    cl.put('D'+str(pin), str(int(value)))

# cl: bridgeclient instance
def communicate(cl):
    global url
    error, response =  commands.getstatusoutput("curl -s " + url)
    if error:
        print "error on curl"
        return

    # print response
    pin_status = json.loads(response)["led"]
    # print "Setting the pin to %s..\n" % pin_status
    setPin(cl, 13, bool(pin_status))

if __name__=="__main__":
    b_client = bridgeclient()
    while True:
        communicate(b_client)
        sleep(0.1)
