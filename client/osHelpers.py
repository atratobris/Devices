import commands
import re

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
    else:
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
    else:
        regex = ".*inet addr:(.*)  Bcast.*"
        lines = wlanInfo.split("\n")
        for line in lines:
            matched = re.match(regex, line)
            if matched:
                return matched.group(1)
    return ""


if __name__ == "__main__" :
    mac = getMacAddress()
    ip = getIpAddress()
    print mac
    print ip
