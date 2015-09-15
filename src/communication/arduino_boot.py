from . import serial_comm
import RPi.GPIO as GPIO
import time

class Arduino():
  PIN_TXD = 14
  PIN_RXD = 15
  

  def resetArduino(self):
    GPIO.setMode(GPIO.BOARD);
    GPIO.setup(PIN_RXD, GPIO.out);
    GPIO.output(PIN_RXD, false);
    time.sleep(1);
    GPIO.output(PIN_RXD, true);


  def handshake(self):
    print("Start handshaking with Arduino")
    is_timed_out = False
    start_millis = int(round(time.time() * 1000))
    ser = serialcomm.SerialCommunication()
    self.resetArduino()
    

    ###########################
    # SENDING HELLO
    ###########################
    ser.serialWrite('2HELO') #hello

    ###########################
    # RECEIVING ACK
    ###########################
    while True:
      message = ser.serialRead()
      if (len(message) == 0):
        current_millis = int(round(time.time() * 1000))
        if (current_millis - start_millis > 10000):   #10 seconds
          is_timed_out = True
          break
      elif (message[0] == '0'): #ACK
        break
      else:
        continue

    if is_timed_out:
      print("Handshaking failed")
      return False

    ###########################
    # SENDING ACK
    ###########################
    ser.serialWrite('0ACK'); #ACK

    return True






        

