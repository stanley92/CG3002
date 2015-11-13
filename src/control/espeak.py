import subprocess
import signal
from collections import deque
#########################################
# espeak class
# + Queue : priority queue
#########################################

class Espeak():
	def __init__(self,prog_controller):
		self.prog_controller = prog_controller
		self.queue_1 = deque() #node
		self.queue_2 = deque() #left-right
		self.queue_3 = None    #immediate
		self.speaking = None
		self.speaking_priority = 4

	def add_speech(self, priority, message):
		if priority == 1:
			self.queue_2.clear()
			self.queue_3 = None
			self.queue_1.append(message)
			self.queue_1.append(message)
			# self.queue.append(priority, subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True))
			# self.queue.append(priority, subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True))
		elif priority == 2:
			self.queue_3 = None
			self.queue_2.append(message)
			# self.queue.append(priority, subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True))
		elif priority == 3:
			self.queue_3 = message
	
	def speak(self):
		while(1):
			try:
				priority = 1
				message = self.queue_1.popleft()
			except IndexError:
				try:
					priority = 2
					message = self.queue_2.popleft()
				except IndexError:
					priority = 3
					message = self.queue_3
			if message != None:
				self.say(priority, message)
			if not self.prog_controller.is_program_running_all():
				print("espeak stopped")
				break


	def say(self, priority, message):
		if priority == 1:
			try:
				if self.speaking_priority > 1:
					self.speaking.send_signal(signal.SIGINT)
					self.speaking = None
			except Exception as e:
				print(str(e))
				pass
			self.speaking_priority = 1
			self.speaking = subprocess.Popen('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True)
		elif priority == 2:
			try:
				if self.speaking_priority > 2:
					self.speaking.send_signal(signal.SIGINT)
					self.speaking = None
			except Exception as e:
				print(str(e))
				pass
			self.speaking_priority = 2
			self.speaking = subprocess.Popen('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True) 
		else:
			self.speaking_priority = 3
			self.speaking = subprocess.Popen('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True) 
    		
