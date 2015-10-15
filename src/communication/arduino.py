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
    self.ser.serialFlush();
    print("Start handshaking with Arduino")
    is_timed_out = False
    start_millis = int(round(time.time() * 1000))
    self._resetArduino()
    print(start_millis)
    


    ###########################
    # SENDING HELLO & RECEIVING HELLOACK
    ###########################
    while True:
      self.ser.serialWrite(chr(2)) #hello
      message = self.ser.serialRead()
      print(chr(ord(message)+48))
      if (message == chr(3)):
        self.ser.serialWrite(chr(0));

        # print("Break")
        break
      else:
        # print("cont")
        current_millis = int(round(time.time() * 1000))
        # print(current_millis)
        if (current_millis - start_millis > 10000):   #10 seconds
          is_timed_out = True
          break

    if is_timed_out:
      print("Handshaking failed")
      return False

    ###########################
    # SENDING ACK
    ###########################
    

    return True

  def get_data(self, callback):
    while True:
      # print("Start getting data")
      is_timed_out = False
      start_millis = int(round(time.time() * 1000))
      # print(start_millis)
      while True:
        message = self.ser.serialRead()

        if (message == chr(6)):
          self.ser.serialWrite(chr(0)); #ACK
          print("Handshaking done")

        if (message == chr(4)): #Write
          break
      print("Got write request")
      while True:
        message = self.ser.serialRead()
        if (message): #Write
          channel = ord(message)
          break
      print("Got channel "+str(channel))
      while True:
        print("read")
        message = self.ser.serialReadLine()
        print("finish reading") 
        if (len(message) != 0): #Write
          break
        else: 
          current_millis = int(round(time.time() * 1000))
          if (current_millis - start_millis > 10000):   #10 seconds
            is_timed_out = True
            break
        if is_timed_out:
          print("Get data Timed Out")
          callback(None, None)
      print("Data got: "+str(message))
      self.ser.serialWrite(chr(0))
      callback(int(channel), message)






        

