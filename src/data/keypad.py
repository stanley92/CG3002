# import subprocess
import time

class KeypadData():
  def __init__(self, speak):
    self.building = None
    self.level = None
    self.start_node = None
    self.end_node = None
    self.current_change = -1
    self.ready = False
    self.current_input = 0
    self.request_query_dist = False
    self.reset_prog = False
    self.speak = speak

  def key_in(self, key):
    print(key);
    if key == '*':
      if self.current_change == -1:
        self.reset_prog = True
        print('program reset')
      self.clear()
      self.speak.add_speech(3, 'clear')
      # self.say('clear')
      print('clear')  
    elif key == '#':
      if self.current_change == -1:
        self.current_change = self.current_change+1
        time.sleep(0.2)
        self.speak.add_speech(3, 'Input Building')
        # self.say('Input Building')
      elif self.current_change == 0:
        self.building = self.current_input
        print('building: '+ str(self.building))
        self.speak.add_speech(3, 'Building. ' + str(self.building))
        # self.say('Building. ' + str(self.building))
        self.current_input = 0
        self.current_change=self.current_change+1
        time.sleep(0.2)
        self.speak.add_speech(3, 'Input Level')
        # self.say('InputLevel')
      elif self.current_change == 1:
        self.level = self.current_input
        print('level: '+ str(self.level))
        self.speak.add_speech(3, 'Level. ' + str(self.level))
        # self.say('Level. ' + str(self.level))
        self.current_input = 0
        self.current_change=self.current_change+1
        time.sleep(0.2)
        self.speak.add_speech(3, 'Input Start node')
        # self.say('Input Start node')
      elif self.current_change == 2:
        self.start_node = self.current_input
        print('start_node: '+ str(self.start_node))
        self.speak.add_speech(3, 'Start Node. ' + str(self.start_node))
        # self.say('Start Node. ' + str(self.start_node))
        time.sleep(0.2)
        self.current_input = 0
        self.current_change=self.current_change+1
        self.speak.add_speech(3, 'Input End node')
        # self.say('Input End node')
      elif self.current_change == 3:  
        self.end_node = self.current_input
        print('end_node: '+ str(self.end_node))
        self.speak.add_speech(3, 'End Node. ' +str(self.end_node))
        time.sleep(0.2)
        # self.say('End Node. ' +str(self.end_node))
        self.current_input = 0
        self.current_change=self.current_change+1
      elif self.current_change == 4:  
        self.ready = True
      

    elif ord(key) in range(ord('0'),ord('9')+1):
      self.speak.add_speech(3, key)
      # self.say(key)
      if self.current_change == -1:
        if ord(key) == ord('9'):
          self.request_query_dist = True
      else:
        self.current_input = self.current_input * 10 + (ord(key)-48)

  def get_building(self):
    return self.building
  def get_level(self):
    return self.level
  def get_start_node(self):
    return self.start_node
  def get_end_node(self):
    return self.end_node

  def data_ready(self):
    return self.ready

  def signal_prog_reset(self):
    if self.reset_prog:
      self.reset_prog = False
      return True
    return self.reset_prog

  def function_query_dist(self):
    if self.request_query_dist:
      self.request_query_dist = False
      return True
    return self.request_query_dist

  # def say(self, message):
  #   subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True) 

  def clear(self):
    self.building = None
    self.level = None
    self.start_node = None
    self.end_node = None
    self.current_change = -1
    self.ready = False
    self.current_input = 0
