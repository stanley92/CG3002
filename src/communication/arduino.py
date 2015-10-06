from . import serial_comm
import RPi.GPIO as GPIO
import time

class Arduino():
  
  def __init__(self, ser):
    self.ser = ser
    self.PIN_TXD = 14
    self.PIN_RXD = 15
  

  def _resetArduino(self):
    # GPIO.setMode(GPIO.BOARD);
    # GPIO.setup(self.PIN_RXD, GPIO.out);
    # GPIO.output(self.PIN_RXD, false);
    time.sleep(1);
    # GPIO.output(self.PIN_RXD, true);


  def handshake(self):
    print("Start handshaking with Arduino")
    is_timed_out = False
    start_millis = int(round(time.time() * 1000))
    self._resetArduino()
    


    ###########################
    # SENDING HELLO & RECEIVING ACK
    ###########################
    while True:
      self.ser.serialWrite(chr(2)) #hello
      message = self.ser.serialRead()
      if (message == chr(0)):
        break
      else:
        current_millis = int(round(time.time() * 1000))
        if (current_millis - start_millis > 10000):   #10 seconds
          is_timed_out = True
          break

    if is_timed_out:
      print("Handshaking failed")
      return False

    ###########################
    # SENDING ACK
    ###########################
    self.ser.serialWrite(chr(0)); #ACK

    return True

  def get_data(self, callback):
    print("Start getting data")
    is_timed_out = False
    start_millis = int(round(time.time() * 1000))
    while True:
      message = self.ser.serialRead()
      if (message[0] == chr(4)): #Write
        self.ser.serialWrite(chr(0))
        break
      else: 
        current_millis = int(round(time.time() * 1000))
        if (current_millis - start_millis > 10000):   #10 seconds
          is_timed_out = True
          break
    if is_timed_out:
      print("Get data Timed Out")
      callback('TIMEOUT')
    print("Data got: "+str(message))
    callback(message)






        

