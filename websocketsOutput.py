#!/usr/bin/python

import thread
import time
import json, sys


sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')
from bridgeclient import BridgeClient as bridgeclient
import websocket

b_client = bridgeclient()

# value: 0 or 1
# pin: integer
# cl: bridgeclient instance
def setPin(cl, pin, value):
    cl.put('D'+str(pin), str(int(value)))

def set_web_socket(url):
    # websocket.enableTrace(True)
    ws = websocket.WebSocketApp( url,
                                on_message = on_message,
                                on_error  = on_error,
                                on_close = on_close,
                                on_open = on_open )
    return ws

def on_message(ws, message):
    print message
    return
    global b_client
    # transform string to json
    message = json.loads(message)

    # this is an activ message from the server
    if "message" in message and "identifier" in message:
        identifier = json.loads(message["identifier"])
        data = message["message"]
        print "{} from {}".format( data["message"], identifier["channel"])
        pin_status = bool(data["message"])
        setPin(b_client, 13, bool(pin_status))
        return

    # get type of message
    if not "type" in message:
        return

    message_type = message["type"]
    # these are all standard messages which are not of any use
    if message_type == "ping":
        return
    elif message_type == "welcome":
        print "Web socket started"
        return
    elif message_type == "confirm_subscription":
        identifier = json.loads(message["identifier"])
        channel = identifier["channel"]
        print "Subscription to channel {} succesful!".format(channel)
        return

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        identifier = {
            "channel":"SketchChannel"
        }
        data = {
            "message":"mama",
            "action":"blink"
        }
        message = {
            "command": "message",
            "identifier":json.dumps(identifier),
            "data": json.dumps(data)
        }

        regards = {
            "command": "subscribe",
            "identifier": json.dumps(identifier)
        }
        ws.send(json.dumps(regards))
        time.sleep(1)

    thread.start_new_thread(run, ())

if __name__ == "__main__":
    ws = set_web_socket("ws://caplatform.herokuapp.com/cable")
    # ws = set_web_socket("ws://localhost:3000/cable")
    ws.run_forever()
