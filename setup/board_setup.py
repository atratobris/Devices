import sys, json, time, thread

sys.path.insert(0, '/usr/lib/python2.7/websocket')

import websocket

SKETCH_CHANNEL = "SketchChannel"
REGISTER_CHANNEL = "RegisterChannel"

RETRY_LIMIT = 20

class BoardSetup():
  def __init__(self, ws_url=None, mac=None, driver=None, deviceType="Input"):
    if ws_url == None:
      return
    self.ws_url = ws_url
    self.mac = mac
    self.driver = driver
    self.deviceType = deviceType

    self.on_open = self._on_open
    self.on_message = self._on_message
    self.on_error = self._on_error
    self.on_close = self._on_close
    self.on_open_callback = self._on_open_callback
    self.on_sketch_message = self._on_sketch_message
    self.on_register_message = self._on_register_message
    self.ws = websocket.WebSocketApp(self.ws_url,
          on_message = self.on_message,
          on_error = self.on_error,
          on_close = self.on_close,
          on_open = self.on_open)
    self.socket_opened = False
    self.registered = False
    self.pending = False
    self.retry_count = RETRY_LIMIT
    self.current_retry = 1
    self.timeout = 1

  def _on_message(self, ws, message):
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

  def _on_register_message(self, ws, message):
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
        self.driver.register_pending()
      else:
        self.pending = False
        self.registered = True
    elif message_type == "deregister_board":
      self.pending = False
      self.registered = False
      self.socket_opened = False
      ws.send(self.unsubscribe(REGISTER_CHANNEL))
      ws.send(self.unsubscribe(SKETCH_CHANNEL))
      print "Closing"
      ws.close()
    else:
      print message
      pass

  def _on_sketch_message(self, ws, message):
    pass

  def _on_error(self, ws, error):
    print error
    self.timeout *= 2
    self.current_retry += 1

  def _on_close(self, ws):
    print '## Closed ##'

  def _on_open(self, ws):
    def run(*args):
      while not self.is_registered():
        if self.is_pending():
          print 'Pending'
          registered_pressed = self.driver.read_register_status()
          if registered_pressed:
            self.register_callback()
        else:
          print "Unregistered %s" % self.mac
          time.sleep(2)
      print 'Registered'
      ws.send(self.greeting(SKETCH_CHANNEL))
      self.on_open_callback(ws, self.check_socket_opened)
    print '## Opened ##'
    print 'Calling Greetings Fn'
    self.timeout = 1
    self.current_retry = 1
    self.registered = False
    self.socket_opened = True
    ws.send(self.greeting(REGISTER_CHANNEL))
    thread.start_new_thread(run, ())

  def _on_open_callback(self, ws, check_socket_opened):
    pass

  def check_socket_opened(self):
    return self.socket_opened


  def set(self, on_open=None, on_close=None, on_message=None, on_error=None, on_open_callback=None, on_sketch_message=None):
    if on_open:
      self.on_open = on_open
    if on_close:
      self.on_close = on_close
    if on_message:
      self.on_message = on_message
    if on_error:
      self.on_error = on_error
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
      self.reset_ws()

  def reset_ws(self):
    self.ws = websocket.WebSocketApp(self.ws_url,
      on_message = self.on_message,
      on_error = self.on_error,
      on_close = self.on_close,
      on_open = self.on_open)

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


  def greeting(self, channel_name):
    regards = {
      'command': 'subscribe',
      'identifier': json.dumps(self.get_identifier(channel_name))
    }

    return json.dumps(regards)

  def unsubscribe(self, channel_name):
    regards = {
      'command': 'unsubscribe',
      'identifier': json.dumps(self.get_identifier(channel_name))
    }

    return json.dumps(regards)

  def get_identifier(self, channel_name):
    obj =  {
      'channel': channel_name,
      'mac': self.mac
    }
    if channel_name == REGISTER_CHANNEL:
        obj["type"] = self.deviceType

    return obj
