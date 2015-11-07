import random
import time
import os
import subprocess
import RPi.GPIO as GPIO
import time

# def poll_data_from_queue():
#   #poll data
class ObstacleDetector():
	def __init__(self, prog_controller, sensorData):
		self.sensors = sensorData
		self.prog_controller = prog_controller
		self.collision_front = False
		self.collision_right_ankle = False
		self.collision_hand = False
		self.collision_left = False
		self.collision_right = False
		self.front_count = 0

	# def collisionWarningDown(self):
	#   if self.sensors.sensor_down > 2000 or self.sensors.sensor_down == 0:
	#     print("Stairs in front")
	#     self.say("Stairs in front")

	# def collisionWarningFront(self): # detect Low Obstacle on the left
	# 	if self.sensors.sensor_front < 70: #and self.sensors.sensor_left_ankle != 0:
	# 		#print ("Low lying obstacle on the left.")
	# 		if not self.collision_hand:
	# 			self.collision_hand = True
	# 			GPIO.output(22, True)
	# 	else:
	# 		if self.collision_hand:
	# 			self.collision_hand = False
	# 			GPIO.output(22, False)
			
	def collisionWarningRightAnkle(self): # detect Low Obstacle on the right
		if self.sensors.sensor_right_ankle < 70: #and self.sensors.sensor_right != 0:
			#print ("Low lying obstacle on the Right.")
			if not self.collision_right_ankle:
				self.collision_right_ankle = True
				GPIO.output(25, True)
		else: 
			if self.collision_right_ankle:
				self.collision_right_ankle = False
				GPIO.output(25, False)

	def collisionWarningHand(self): # detect obstacle with hand
		if self.sensors.sensor_hand < 70: #and self.sensors.sensor_hand != 0:
			#print ("There is obstacle in front.")
			if not self.collision_hand:
				self.collision_hand = True
				GPIO.output(23, True)
		else: 
			if self.collision_hand:
				self.collision_hand = False
				GPIO.output(23, False)

	def collisionWarningFront(self): 
		if self.sensors.sensor_front < 70: #and self.sensors.sensor_front != 0:
			#print ("Obsatcle on the front.")
			if not self.collision_front:
				self.collision_front = True
				GPIO.output(22, True)
		else: 
			if self.collision_front:
				self.collision_front = False
				GPIO.output(22, False)

		# if self.collision_front == True and self.sensors.sensor_front < 40:
		# 		self.front_count = self.front_count + 1
		# 		if self.front_count == 5:
		# 			self.front_count = 0
		# 		if self.front_count == 0:
		# 			self.say('Front obstacle is very near')
		# 	elif self.collision_front == False:
		# 		self.front_count = 0

	def collisionWarningLeft(self): 
		if self.sensors.sensor_left < 70: #and self.sensors.sensor_left != 0:
			#print ("Obstacle on the left.")
			if not self.collision_left:
				self.collision_left = True
				GPIO.output(27, True)
		else: 
			if self.collision_left:
				self.collision_left = False
				GPIO.output(27, False)

	def collisionWarningRight(self): 
		if self.sensors.sensor_right < 60: #and self.sensors.sensor_left != 0:
			#print ("Obsatcle on the right.")
			if not self.collision_right:
				self.collision_right = True
				GPIO.output(24, True)
		else: 
			if self.collision_right:
				self.collision_right = False
				GPIO.output(24, False)


	def inf_loop1(self):
		while True:
			# print(
			# 	str(self.sensors.sensor_hand)+" "+
			# 	str(self.sensors.sensor_left)+" "+
			# 	str(self.sensors.sensor_right)+" "+
			# 	str(self.sensors.sensor_front)+" "+
			# 	str(self.sensors.sensor_right_ankle))
			# time.sleep(2)
			
			self.collisionWarningRight()
			if not self.prog_controller.is_program_running_sim():
				print('ObstacleDetector stopped')
				break
			time.sleep(0.2)

	def inf_loop2(self):

		while True:
			self.collisionWarningRightAnkle()
			if not self.prog_controller.is_program_running_sim():
				print('ObstacleDetector stopped')
				break
			time.sleep(0.2)

	def inf_loop3(self):
		while True:
			self.collisionWarningHand()
			if not self.prog_controller.is_program_running_sim():
				print('ObstacleDetector stopped')
				break
			time.sleep(0.2)

	def inf_loop4(self):
		while True:
			self.collisionWarningLeft()
			if not self.prog_controller.is_program_running_sim():
				print('ObstacleDetector stopped')
				break
			time.sleep(0.2)

	def inf_loop5(self):
		while True:
			self.collisionWarningFront()
			if not self.prog_controller.is_program_running_sim():
				print('ObstacleDetector stopped')
				break
			time.sleep(0.2)


