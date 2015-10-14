from . import arduino
from . import serial_comm
from . import data_buffer
import threading

def read_from_port(buf):
  buf.buffer()

def main():
  ser = serial_comm.SerialCommunication()
  ard = arduino.Arduino(ser)
  if ard.handshake():
    buf = data_buffer.DataBuffer(5, ard)
    thread = threading.Thread(target=read_from_port,args=[buf])
    thread.start()
  
if __name__ == '__main__':
  main()
