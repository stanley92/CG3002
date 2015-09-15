import serial

class SerialCommunication():
  def __init__(self):
    self.port = serial.Serial('/dev/ttyAMA0', baudrate=115220)
    self.port.open()

  def serialWrite(self, message):
    self.port.write(message)
    return

  def serialRead(self):
    return self.port.readline()
