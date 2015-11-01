import subprocess
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

	def add_speech(self, priority, message):
		if priority == 1:
			self.queue_2.clear()
			self.queue_3 = None
			self.queue_1.put(message)
			self.queue_1.put(message)
			# self.queue.put(priority, subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True))
			# self.queue.put(priority, subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', arrivedText), shell=True))
		elif priority == 2:
			self.queue_3 = None
			self.queue_2.put(message)
			# self.queue.put(priority, subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True))
		elif priority == 3:
			self.queue_3 = message
	
	def speak(self):
		while(1):
			try:
				priority = 1
				message = self.queue_1.pop()
			except IndexError:
				try:
					priority = 2
					message = self.queue_2.pop()
				except IndexError:
					priority = 3
					message = self.queue_3
			if message != None:
				self.say(priority, message)
			if not prog_controller.is_program_running_all():
				print("espeak stopped")
				break


	def say(self, priority, message):
		if priority == 1:
			subprocess.call('espeak -v%s+%s -s120 "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True)
		else:
			subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True) 
    		
