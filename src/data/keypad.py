# import subprocess
import time

class KeypadData():
  def __init__(self, speak):
    self.start_building = None
    self.start_level = None
    self.start_node = None
    self.end_building = None
    self.end_level = None
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
      print('clear')  
    elif key == '#':
      if self.current_change == -1:
        self.current_change = self.current_change+1
        time.sleep(0.5)
        self.speak.add_speech(3, 'Input Start Building')
      elif self.current_change == 0:
        self.start_building = self.current_input
        print('start_building: '+ str(self.start_building))
        self.speak.add_speech(3, 'Start Building. ' + str(self.start_building))
        self.current_input = 0
        self.current_change=self.current_change+1
        time.sleep(0.5)
        self.speak.add_speech(3, 'Input Start Level')
      elif self.current_change == 1:
        self.start_level = self.current_input
        print('start_level: '+ str(self.start_level))
        self.speak.add_speech(3, 'Start Level. ' + str(self.start_level))
        self.current_input = 0
        self.current_change=self.current_change+1
        time.sleep(0.5)
        self.speak.add_speech(3, 'Input Start node')
      elif self.current_change == 2:
        self.start_node = self.current_input
        print('start_node: '+ str(self.start_node))
        self.speak.add_speech(3, 'Start Node. ' + str(self.start_node))
        time.sleep(0.5)
        self.current_input = 0
        self.current_change=self.current_change+1
        self.speak.add_speech(3, 'Input End Building')
      elif self.current_change == 3:  
        self.end_building = self.current_input
        print('end_building: '+ str(self.end_building))
        self.speak.add_speech(3, 'End Building. ' +str(self.end_node))
        time.sleep(0.5)
        self.current_input = 0
        self.current_change=self.current_change+1
        self.speak.add_speech(3, 'Input End Level')
      elif self.current_change == 4:  
        self.end_level = self.current_input
        print('end_level: '+ str(self.end_level))
        self.speak.add_speech(3, 'End Level. ' +str(self.end_node))
        time.sleep(0.5)
        self.current_input = 0
        self.current_change=self.current_change+1
        self.speak.add_speech(3, 'Input End Node')
      elif self.current_change == 5:  
        self.end_node = self.current_input
        print('end_node: '+ str(self.end_node))
        self.speak.add_speech(3, 'End Node. ' +str(self.end_node))
        time.sleep(0.5)
        self.current_input = 0
        self.current_change=self.current_change+1
        self.speak.add_speech(3, 'Press # to start')
      elif self.current_change == 6:  
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
    return self.start_building
  def get_level(self):
    return self.start_level
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
    self.start_building = None
    self.start_level = None
    self.start_node = None
    self.end_building = None
    self.end_level = None
    self.end_node = None
    self.current_change = -1
    self.ready = False
    self.current_input = 0
