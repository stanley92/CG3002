import sensors
import threading
import random
import time
import os

# def poll_data_from_queue():
# 	#poll data

def collisionWarningDown(s):
  if s.sensorDown < 30 and s.sensorDown != 0:
	  os.system("say Stairs in front")

def collisionWarningLeft(s): #1
	if s.sensorLeft < 30 and s.sensorLeft != 0:
		print ("There is obstacle on the left.")
		return 1
	else: 
		return 0

def collisionWarningRight(s):
  if s.sensorRight < 30 and s.sensorRight != 0:
    print ("There is obstacle on the Right.")
    return 1
  else:
    return 0

def collisionWarningFront(s): #3
  if s.sensorFront < 30 and s.sensorFront != 0:
    print ("There is obstacle in front.")
    return 1
  else:
    return 0

def collisionWarningLeg(s): #4
  if s.sensorLeg < 30 and s.sensorLeg != 0:
    print ("Low lying obstacle.")
    return 1
  else: 
    return 0

def inf_loop(s):
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

def run():
	#print("hi")
	s = sensors.Sensors()
	t = threading.Thread(target=inf_loop,args=[s])
	t.start()
	#t.delay(100)

run()