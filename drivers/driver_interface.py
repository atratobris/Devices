class DriverInterface():
  def __init__(self):
    raise NotImplementedError( "Should have implemented this" )

  def register_pending(self):
    raise NotImplementedError( "Should have implemented this" )

  def read_register_status(self):
    raise NotImplementedError( "Should have implemented this" )

  def get(self):
    raise NotImplementedError( "Should have implemented this" )

  def reset(self):
    raise NotImplementedError( "Should have implemented this" )

  def set(self):
    raise NotImplementedError( "Should have implemented this" )    