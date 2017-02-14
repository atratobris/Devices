#!/usr/bin/python
import sys
sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')
import thread, time, json, os, websocket, commands, re
b_client = None

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


# value: 0 or 1 | pin: integer | cl: bridgeclient instance
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
    global b_client
    # transform string to json
    message = json.loads(message)

    # this is an active message from the server
    if "message" in message and "identifier" in message:
        identifier = json.loads(message["identifier"])
        data = message["message"]
        print "{} from {}".format( data["message"], identifier["channel"])
        pin_status = bool(data["message"])
        if Config.embedded():
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
            "channel":"SketchChannel",
            "mac": Config.getMac()
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
    if Config.embedded():
        ws = set_web_socket("ws://caplatform.herokuapp.com/cable")
    else:
        ws = set_web_socket("ws://localhost:3000/cable")
    ws.run_forever()
