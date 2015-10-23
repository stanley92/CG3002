class KeypadData():
  def __init__(self):
    self.building = None
    self.level = None
    self.start_node = None
    self.end_node = None
    self.current_change = -1
    self.ready = False
    self.current_input = 0
    self.request_query_dist = False

  def key_in(self, key):
    print(key);
    if key == '*':
      self.clear()
      self.say('clear')
      print('clear')  
    elif key == '#':
      if self.current_change == -1:
        self.current_change = self.current_change+1
      elif self.current_change == 0:
        self.building = self.current_input
        print('building: '+ str(self.building))
        self.say(str(self.building))
        self.current_input = 0
        self.current_change=self.current_change+1
      elif self.current_change == 1:
        self.level = self.current_input
        print('level: '+ str(self.level))
        self.say(str(self.level))
        self.current_input = 0
        self.current_change=self.current_change+1
      elif self.current_change == 2:
        self.start_node = self.current_input
        print('start_node: '+ str(self.start_node))
        self.say(str(self.start_node))
        self.current_input = 0
        self.current_change=self.current_change+1
      elif self.current_change == 3:  
        self.end_node = self.current_input
        print('end_node: '+ str(self.end_node))
        self.say(str(self.end_node))
        self.current_input = 0
        self.current_change=self.current_change+1
        self.ready = True
      

    elif ord(key) in range(ord('0'),ord('9')+1):
      self.say(key)
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

  def function_query_dist(self):
    if self.request_query_dist:
      self.request_query_dist = False
      return True
    return self.request_query_dist

  def say(self, message):
    subprocess.call('espeak -v%s+%s "%s" 2>/dev/null' % ('en-us', 'f3', message), shell=True) 

  def clear(self):
    self.building = None
    self.level = None
    self.start_node = None
    self.end_node = None
    self.current_change = -1
    self.ready = False
    self.current_input = 0
