import Queue

class DataBuffer():
  def __init__(self, ard):
    self.mQueue = Queue.Queue()
    self.ard = ard

  def push(self, m):
    self.mQueue.put(m)
  
  def buffer(self):
    self.ard.get_data(self.push)

  def poll(self):
    self.mQueue.get()
