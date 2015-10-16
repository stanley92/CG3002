from collections import deque

class DataBuffer():
  def __init__(self, num_queue, ard):
    self.queues = num_queue*[0]
    for i in range(num_queue):
      self.queues[i] = deque()
    self.ard = ard

  def push(self, channel, m):
    if (channel != None and m != None):
      self.queues[channel].append(m)
  
  def buffer(self):
    self.ard.get_data(self.push)

  def pop(self, channel):
    try:
      return self.queues[channel].popleft()
    except IndexError:
      return None

  def last(self, channel):
    try:
      return self.queues[channel].pop()
    except IndexError:
      return None

  def clear(self, channel):
    self.queues[channel].clear()

  def pop_all(self, channel):
    all_data = []
    while True:
      try:
        all_data.append(self.queues[channel].pop());
      except IndexError:
        return all_data

  def have_data(self, channel):
    return bool(self.queues[channel])
