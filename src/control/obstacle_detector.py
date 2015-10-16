import threading
import random
import time
import os
import subprocess
import RPi.GPIO as GPIO

# def poll_data_from_queue():
# 	#poll data
class ObstacleDetector():
  def __init__(self, sensorData):
    self.sensors = sensorData

  def collisionWarningDown(self):
    if self.sensors.sensorDown > 2000 or self.sensors.sensorDown != 0:
  	  say("Stairs in front")

  def collisionWarningLeft(self): #1
  	if self.sensors.sensorLeft < 70 and self.sensors.sensorLeft != 0:
  		print ("There is obstacle on the left.")
  		GPIO.output(23, True)
  	else: 
      		GPIO.output(23, False)

  def collisionWarningRight(self):
    if self.sensors.sensorRight < 70 and self.sensors.sensorRight != 0:
      print ("There is obstacle on the Right.")
      GPIO.output(24, True)
    else: 
      GPIO.output(24, False)

  def collisionWarningFront(self): #3
    if self.sensors.sensorFront < 70 and self.sensors.sensorFront != 0:
      print ("There is obstacle in front.")
      GPIO.output(22, True)
    else: 
      GPIO.output(22, False)

  def collisionWarningLeg(self): #4
    if self.sensors.sensorLeg < 70 and self.sensors.sensorLeg != 0:
      print ("Low lying obstacle.")
      GPIO.output(27, True)
    else: 
      GPIO.output(27, False)

  def inf_loop(self):
  	while (1):
  		#poll_data_from_queue()
  		# valueDown = random.randint (0,100)
  		# s.setSensorDown(valueDown)
  		
  		# valueLeft = random.randint (0,100)
  		# s.setSensorLeft(valueLeft)
  		
  		# valueRight = random.randint (0,100)
  		# s.setSensorRight(valueRight)
  		
  		# valueFront = random.randint (0,100)
  		# s.setSensorFront(valueFront)
  		
  		# valueLeg = random.randint (0,100)
  		# s.setSensorLeg(valueLeg)
  		
  		#print ("Value: " + str (value))
  		collisionWarningDown(s)
  		collisionWarningRight(s)
  		collisionWarningFront(s)
  		collisionWarningLeg(s)
  		collisionWarningLeft(s)

  		time.sleep(1)
  		print('')
  
  def say(self, message):
    subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f4', message), shell=True) 

  def run(self):
  	#print("hi")
  	t = threading.Thread(target=self.inf_loop,args=[])
  	t.start()
  	#t.delay(100)

