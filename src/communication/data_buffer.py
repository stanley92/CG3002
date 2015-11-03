from collections import deque
import logging 
class DataBuffer():
  def __init__(self, num_queue, ard):
    self.queues = num_queue*[0]
    for i in range(3):
      self.queues[i] = deque()
    self.ard = ard
    

  def push(self, channel, m):
    try:
      if (channel != None and m != None):
        if (channel in range(3)):
          self.queues[channel].append(m)
        else:
          self.queues[channel] = m
    except IndexError:
      print("Index Error")
      print("channel = " + str(channel))
      print("message = " + m)
  
  def buffer(self):
    self.ard.get_data(self.push)

  def pop(self, channel):
    try:
      if (channel in range(3)):
        return self.queues[channel].popleft()
      else:
        m = self.queues[channel]
        self.queues[channel] = None
        return m
    except IndexError:
      return None

  def last(self, channel):
    try:
      if (channel in range(3)):
        return self.queues[channel].pop()
      else:
        m = self.queues[channel]
        self.queues[channel] = None
        return m
    except IndexError:
      return None

  def clear(self, channel):
    if (channel in range(3)):
      self.queues[channel].clear()
    else:
      self.queues[channel] = None

  def pop_all(self, channel):
    all_data = []
    while True:
      try:
        if (channel in range(3)):
          all_data.append(self.queues[channel].pop());
        else:
          m = self.queues[channel]
          self.queues[channel] = None
          return m
      except IndexError:
        return all_data

  def have_data(self, channel):
    if (channel in range(3)):
      return bool(self.queues[channel])
    else:
      return self.queues[channel] != None
    
