import random
import time
import os
import subprocess
import RPi.GPIO as GPIO

# def poll_data_from_queue():
# 	#poll data
class ObstacleDetector():
  def __init__(self, prog_controller, sensorData):
    self.sensors = sensorData
    self.prog_controller = prog_controller

  # def collisionWarningDown(self):
  #   if self.sensors.sensor_down > 2000 or self.sensors.sensor_down == 0:
  #     print("Stairs in front")
  #     self.say("Stairs in front")

  def collisionWarningLeftAnkle(self): # detect Low Obstacle on the left
  	if self.sensors.sensor_left_ankle < 60: #and self.sensors.sensor_left_ankle != 0:
  		#print ("Low lying obstacle on the left.")
  		GPIO.output(23, True)
  	else:
		GPIO.output(23, False)
 
  def collisionWarningRightAnkle(self): # detect Low Obstacle on the right
    if self.sensors.sensor_right_ankle < 60: #and self.sensors.sensor_right != 0:
      #print ("Low lying obstacle on the Right.")
      GPIO.output(25, True)
    else: 
      GPIO.output(25, False)

  def collisionWarningHand(self): # detect obstacle with hand
    if self.sensors.sensor_hand < 40: #and self.sensors.sensor_hand != 0:
      #print ("There is obstacle in front.")
      GPIO.output(22, True)
    else: 
      GPIO.output(22, False)

  def collisionWarningLeft(self): 
    if self.sensors.sensor_left < 60: #and self.sensors.sensor_left != 0:
      #print ("Obstacle on the left.")
      GPIO.output(27, True)
    else: 
      GPIO.output(27, False)

  def collisionWarningRight(self): 
    if self.sensors.sensor_right < 60: #and self.sensors.sensor_left != 0:
      #print ("Obsatcle on the right.")
      GPIO.output(24, True)
    else: 
      GPIO.output(24, False)

  def inf_loop(self):
  	while True:
  		#poll_data_from_queue()
  		# valueDown = random.randint (0,100)
  		# s.setSensorDown(valueDown)
  		
  		# valueLeft = random.randint (0,100)
  		# s.setSensorLeft(valueLeft)
  		
  		# valueRight = random.randint (0,100)
  		# s.setSensorRight(wvalueRight)
  		
  		# valueFront = random.randint (0,100)
  		# s.setSensorFront(valueFront)
  		
  		# valueLeg = random.randint (0,100)
  		# s.setSensorLeg(valueLeg)
  		
  		#print ("Value: " + str (value))
  		self.collisionWarningRight()
  		self.collisionWarningRightAnkle()
  		self.collisionWarningHand()
  		self.collisionWarningLeft()
  		self.collisionWarningLeftAnkle()
      time.sleep(0.1)
  		if not self.prog_controller.is_program_running():
		    print('ObstacleDetector stopped')
        break
  
  def say(self, message):
    subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f4', message), shell=True) 


