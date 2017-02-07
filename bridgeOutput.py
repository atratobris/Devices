#!/usr/bin/python

import sys
sys.path.insert(0, '/usr/lib/python2.7/bridge')

from time import sleep
from bridgeclient import BridgeClient as bridgeclient

url  = 'http://captest.ngrok.io/api/board.json'

# cl: bridgeclient instance
def blink(cl):
    cl.put('D12','0')
    cl.put('D13','1')
    sleep(0.1)
    cl.put('D12','1')
    cl.put('D13','0')
    sleep(0.1)

print("I hope you enjoyed the light show\n")

# value: 0 or 1
# pin: integer
# cl: bridgeclient instance
def setPin(cl, pin, value):
    value.put('D'+str(pin), str(value))

# cl: bridgeclient instance
def communicate(cl):
    _, response =  commands.getstatusoutput("curl -s " + url)
    pin_status = json.loads(response)["led"]
    print "Setting the pin to %s..\n" % pin_status
    setPin(ip, 13, pin_status)

if __name__=="__main__":
    b_client = bridgeclient()
    while True:
        blink(b_client)
