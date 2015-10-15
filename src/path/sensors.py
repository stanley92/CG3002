
class Sensors():
  def __init__(self):
    # values are in cm
    self.sensorLeft = 0
    self.sensorDown = 0
    self.sensorFront = 0
    self.sensorRight = 0
    self.sensorLeg = 0

  def setSensorLeft(self,v): #1
    self.sensorLeft = v

  def setSensorDown(self,v): #2
    self.sensorDown = v 

  def setSensorFront(self,v): #3
    self.sensorFront = v

  def setSensorRight(self,v): #4
    self.sensorRight = v
  
  def setSensorLeg(self,v): #5
    self.sensorLeg = v  

