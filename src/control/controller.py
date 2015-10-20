class Controller():
  def __init__(self): 
    self.running = False

  def start(self):
    self.running = True

  def end(self):
    self.running = False

  def is_program_running(self):
    return self.running