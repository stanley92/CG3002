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
    if self.sensors.sensor_down > 2000 or self.sensors.sensor_down != 0:
      print("Stairs in front")
      self.say("Stairs in front")

  def collisionWarningLeft(self): #1
  	if self.sensors.sensor_left < 70 and self.sensors.sensor_left != 0:
  		print ("There is obstacle on the left.")
  		GPIO.output(23, True)
  	else:
      GPIO.output(23, False)

  def collisionWarningRight(self):
    if self.sensors.sensor_right < 70 and self.sensors.sensor_right != 0:
      print ("There is obstacle on the Right.")
      GPIO.output(24, True)
    else: 
      GPIO.output(24, False)

  def collisionWarningFront(self): #3
    if self.sensors.sensor_front < 70 and self.sensors.sensor_front != 0:
      print ("There is obstacle in front.")
      GPIO.output(22, True)
    else: 
      GPIO.output(22, False)

  def collisionWarningLeg(self): #4
    if self.sensors.sensor_leg < 70 and self.sensors.sensor_leg != 0:
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
  		self.collisionWarningDown()
  		self.collisionWarningRight()
  		self.collisionWarningFront()
  		self.collisionWarningLeg()
  		self.collisionWarningLeft()
  		print('')
  
  def say(self, message):
    subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f4', message), shell=True) 

  def run(self):
  	#print("hi")
  	t = threading.Thread(target=self.inf_loop,args=[])
  	t.start()
  	#t.delay(100)

