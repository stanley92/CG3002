import serial

class SerialCommunication():
  def __init__(self):
    self.port = serial.Serial('/dev/ttyAMA0', baudrate=115200, timeout=1)
    self.port.open()

  def serialWrite(self, message):
    self.port.write(message)
    return

  def serialRead(self):
    return self.port.read()

  def serialFlush(self):
    return self.port.flush()

  def serialReadLine(self):
    rv=""
    while True:
      ch=self.port.read()
      rv+=ch
      if ch=='\r' or ch=='\0':
        return rv
