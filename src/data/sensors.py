
class Sensors():
  def __init__(self):
    # values are in cm
    self.sensor_left = 0
    self.sensor_down = 0
    self.sensor_front = 0
    self.sensor_right = 0
    self.sensor_leg = 0

  def set_sensor_left(self,v): #1
    self.sensor_left = v

  def set_sensor_down(self,v): #2
    self.sensor_down = v 

  def set_sensor_front(self,v): #3
    self.sensor_front = v

  def set_sensor_right(self,v): #4
    self.sensor_right = v
  
  def set_sensor_leg(self,v): #5
    self.sensor_leg = v  

