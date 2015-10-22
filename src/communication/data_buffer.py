from collections import deque
import logging 
class DataBuffer():
  def __init__(self, num_queue, ard):
    self.queues = num_queue*[0]
    for i in range(num_queue):
      self.queues[i] = deque()
    self.ard = ard
    logging.basicConfig(filename='databuffer.log', level=logging.DEBUG)
    logging.debug('***** START BUFFER *****')

  def push(self, channel, m):
    try:
      if (channel != None and m != None):
        self.queues[channel].append(m)
    except IndexError:
      print("Index Error")
      print("channel = " + str(channel))
      print("message = " + m)
      logging.ERROR("Index Error")
      logging.ERROR("channel = " + str(channel))
      logging.ERROR("message = " + m)
  
  def buffer(self):
    self.ard.get_data(self.push)

  def pop(self, channel):
    try:
      return self.queues[channel].popleft()
    except IndexError:
      return None

  def last(self, channel):
    try:
      message = self.queues[channel].pop()
      logging.debug('Channel '+str(channel)+' latest data acknowledged ~ : "'+str(message)+'"')
      return message
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
