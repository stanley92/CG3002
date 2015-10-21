
class Sensors():
  def __init__(self):
    # values are in cm
    self.sensor_hand = 0
    self.sensor_left = 0
    self.sensor_right = 0
    self.sensor_left_ankle = 0
    self.sensor_right_ankle = 0

  def set_sensor_left(self,v): #1
    self.sensor_hand = v

  def set_sensor_down(self,v): #2
    self.sensor_left = v 

  def set_sensor_front(self,v): #3
    self.sensor_right = v

  def set_sensor_right(self,v): #4
    self.sensor_left_ankle = v
  
  def set_sensor_leg(self,v): #5
    self.sensor_right_ankle = v  

