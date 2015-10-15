from . import communication
from communication import communication

def test():
  c = communication.Communication()
  c.initialise()
  return c