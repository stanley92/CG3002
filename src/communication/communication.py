from . import arduino
from . import serial_comm
from . import data_buffer
import threading

class Communication():
  def __init__(self, prog_controller):
    self.ser = serial_comm.SerialCommunication()
    self.prog_controller = prog_controller
    self.ard = arduino.Arduino(self.ser)
    self.handshaken = False
    self.buffer = None
    self.thread = None

  def read_from_port(self):
    while True:
      self.buffer.buffer()
      if not self.prog_controller.is_program_running_all():
        print("Data buffering stopped")
        break

  def initialise(self, num_queue=9):
    #self.handshaken = self.ard.handshake()
    self.handshaken = True
    if self.handshaken:
      self.buffer = data_buffer.DataBuffer(num_queue, self.ard)
      self.thread = threading.Thread(target=self.read_from_port,args=[])
      self.thread.start()
    return self.handshaken # False means failed
    
  def pop_next(self, queue_number):
    return self.buffer.pop(queue_number)

  def pop_latest(self, queue_number):
    return self.buffer.last(  queue_number)

  def flush(self, queue_number):
    return self.buffer.clear(queue_number)

  def pop_all(self, queue_number):
    return self.buffer.pop_all(queue_number)

