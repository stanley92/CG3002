from . import arduino
from . import serial_comm
from . import data_buffer
import threading

class Communication():
  def __init__():
    self.ser = serial_comm.SerialCommunication()
    self.ard = arduino.Arduino(ser)
    self.handshaken = False
    self.buffer = None
    self.thread = None

  def read_from_port(buf):
    buf.buffer()

  def initialise(self, num_queue=5):
    self.handshaken = ard.handshake()
    if self.handshaken:
      self.buffer = data_buffer.DataBuffer(ard, num_queue)
      self.thread = threading.Thread(target=read_from_port,args=[buf])
      self.thread.start()
    return self.handshaken # False means failed
    
  def pop_next(self, queue_number):
    return self.buffer.pop(queue_number)

  def pop_latest(self, queue_number):
    return self.buffer.last(queue_number)

  def flush(self, queue_number):
    return self.buffer.clear(queue_number)

  def pop_all(self, queue_number):
    return self.buffer.pop_all(queue_number)
