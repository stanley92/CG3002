
class obstacle():
  def __init__(self):
    self.sensorL = 0 # values are in cm
    self.sensorR = 0
    self.sensorF = 0
    self.sensorB = 0

  def setSensorL(self,v):
    self.sensorL = v

  def setSensorR(self,v):
    self.sensorR = v

  def setSensorF(self,v):
    self.sensorF = v

  def setSensorB(self,v):
    self.sensorB = v

  def collisionWarningL(self):
    if self.sensorR < 30:
      return 1

  def collisionWarningR(self):
    if self.sensorR < 30:
      return 1

  def collisionWarningF(self):
    if self.sensorR < 30:
      return 1

  def collisionWarningB(self):
    if self.sensorR < 30:
      return 1
