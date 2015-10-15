import threading
import random
import time
import os

# def poll_data_from_queue():
# 	#poll data
def ObstacleDetector():
  def __init__(self, sensorData):
    self.sensors = sensorData

  def collisionWarningDown(self):
    if self.sensors.sensorDown < 30 and self.sensors.sensorDown != 0:
  	  os.system("say Stairs in front")

  def collisionWarningLeft(self): #1
  	if self.sensors.sensorLeft < 30 and self.sensors.sensorLeft != 0:
  		print ("There is obstacle on the left.")
  		return 1
  	else: 
  		return 0

  def collisionWarningRight(self):
    if self.sensors.sensorRight < 30 and self.sensors.sensorRight != 0:
      print ("There is obstacle on the Right.")
      return 1
    else:
      return 0

  def collisionWarningFront(self): #3
    if self.sensors.sensorFront < 30 and self.sensors.sensorFront != 0:
      print ("There is obstacle in front.")
      return 1
    else:
      return 0

  def collisionWarningLeg(self): #4
    if self.sensors.sensorLeg < 30 and self.sensors.sensorLeg != 0:
      print ("Low lying obstacle.")
      return 1
    else: 
      return 0

  def inf_loop(self):
  	while (1):
  		#poll_data_from_queue()
  		valueDown = random.randint (0,100)
  		s.setSensorDown(valueDown)
  		
  		valueLeft = random.randint (0,100)
  		s.setSensorLeft(valueLeft)
  		
  		valueRight = random.randint (0,100)
  		s.setSensorRight(valueRight)
  		
  		valueFront = random.randint (0,100)
  		s.setSensorFront(valueFront)
  		
  		valueLeg = random.randint (0,100)
  		s.setSensorLeg(valueLeg)
  		
  		#print ("Value: " + str (value))
  		collisionWarningDown(s)
  		collisionWarningRight(s)
  		collisionWarningFront(s)
  		collisionWarningLeg(s)
  		collisionWarningLeft(s)

  		time.sleep(1)
  		print('')

  def run(self):
  	#print("hi")
  	t = threading.Thread(target=self.inf_loop,args=[])
  	t.start()
  	#t.delay(100)

