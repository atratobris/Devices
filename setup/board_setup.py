import sys, json, time

sys.path.insert(0, '/usr/lib/python2.7/websocket')
sys.path.insert(0, '/usr/lib/python2.7/bridge')

import websocket

SKETCH_CHANNEL = "SketchChannel"
REGISTER_CHANNEL = "RegisterChannel"

RETRY_LIMIT = 20

class BoardSetup():
  def __init__(self, ws_url=None, mac=None):
    if ws_url == None:
      return
    self.ws_url = ws_url
    websocket.enableTrace(False);
    self.ws = websocket.WebSocketApp(self.ws_url,
          on_message = self.on_message,
          on_error = self.on_error,
          on_close = self.on_close,
          on_open = self.on_open)
    self.registered = False
    self.pending = False
    self.mac = mac
    self.retry_count = RETRY_LIMIT
    self.current_retry = 1
    self.timeout = 1

  def on_message(self, ws, message):
    message_object = json.loads(message)
    message_type = message_object.get("type", "unknown")

    if message_type == 'confirm_subscription':
      print message_object
    elif message_type == 'ping':
      pass
    else:
      identifier = message_object.get('identifier', {})
      channel = ''
      try:
        identifier = json.loads(identifier.encode('utf-8'))
        channel = identifier.get('channel', '')
      except Exception as e:
        print "Error at " + str(identifier)
      if channel == REGISTER_CHANNEL:
        self.on_register_message(ws, message_object)
      elif channel == SKETCH_CHANNEL:
        self.on_sketch_message(ws, message_object)
      else:
        print message

  def on_register_message(self, ws, message):
    message_object = message.get("message", {})
    message_type = message_object.get("type", "unknown")
    if message_type == "board_details":
      board = message_object.get("board", {})
      if board.get('mac', '') != self.mac:
        return
      register_status = board.get("register_status", 'unregistered')
      if register_status == 'unregistered':
        pass
      elif register_status == 'pending':
        self.pending = True
      else:

        self.pending = False
        self.registered = True
    else:
      print message
      pass

  def on_sketch_message(self, ws, message):
    pass

  def on_error(self, ws, error):
    print error
    self.timeout *= 2
    self.current_retry += 1

  def on_close(self, ws):
    print '## Closed ##'

  def on_open(self, ws):
    print '## Opened ##'
    print 'Calling Greetings Fn'
    self.timeout = 1
    self.current_retry = 1
    ws.send(self.register_greeting())
    self.registered = False
    self.on_open_callback(ws, self.is_registered, self.is_pending, self.register_callback)

  def on_open_callback(self, ws, is_registered, is_pending, register_callback):
    pass

  def set(self, on_open=None, on_close=None, on_message=None, on_error=None, on_open_callback=None, on_sketch_message=None):
    if on_open:
      self.ws.on_open = on_open
    if on_close:
      self.ws.on_close = on_close
    if on_message:
      self.ws.on_message = on_message
    if on_error:
      self.ws.on_error = on_error
    if on_open_callback:
      self.on_open_callback = on_open_callback
    if on_sketch_message:
      self.on_sketch_message = on_sketch_message

  def is_registered(self):
    return self.registered

  def is_pending(self):
    return self.pending

  def run_forever(self):
    while (self.current_retry < self.retry_count):
      self.ws.run_forever()
      time.sleep(self.timeout)
      print "Sleeping for " + str(self.timeout)



  def register_callback(self):
    self.ws.send(self.register_message())

  def register_message(self):
    data = {
      'action': 'register'
    }
    message = {
      'command': 'message',
      'identifier': json.dumps(self.get_identifier(REGISTER_CHANNEL)),
      'data': json.dumps(data)
    }

    return json.dumps(message)


  def register_greeting(self):
    regards = {
      'command': 'subscribe',
      'identifier': json.dumps(self.get_identifier(REGISTER_CHANNEL))
    }

    return json.dumps(regards)

  def get_identifier(self, channel_name):
    return {
      'channel': channel_name,
      'mac': self.mac
    }



