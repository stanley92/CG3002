class Controller():
  def __init__(self): 
    self.running_all = False

  def start_all(self):
    self.running_all = True
    self.running_sim = True

  def start_sim(self):
  	self.running_sim = True

  def stop_all(self):
    self.running_sim = False
    self.running_all = False

  def stop_sim(self):
    self.running_sim = False

  def is_program_running_all(self):
    return self.running_all

  def is_program_running_sim(self):
    return self.running_all and self.running_sim